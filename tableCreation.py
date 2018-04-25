import os
import os.path
import cobra
import pandas
import pymysql
import cgi
import cgitb
from sqlalchemy import create_engine
cgitb.enable()

# Methods
def loadingAgora(directory):
    # get all the model files in the agora folder, hold in a list
    model_files = os.listdir(directory)[0:1]
    return model_files

def addToReactions(reaction, current_model_id, current_reaction_id, REACTIONS, MOD_REACT):
    name = reaction.id
    str_name = reaction.name
    try:
        ec = reaction.annotation['ec-code']
    except KeyError:
        ec = "NULL"  
    REACTIONS = REACTIONS.append({"RID": current_reaction_id ,"NAME": name, "Str_NAME": str_name, "ec-code": ec}, ignore_index=True)
    MOD_REACT = MOD_REACT.append( { "MID": current_model_id, "RID": current_reaction_id }, ignore_index=True)
    return REACTIONS, MOD_REACT

def addToMetabolites(metID, officialName, met, model, METABOLITES):
    str_name = met.name
    compartment = met.compartment 
    
    try:
        kegg = model.metabolites.get_by_id(met.id).annotation["kegg.compound"]
    except KeyError:
        kegg = "NULL"
    try:
        pubchem = model.metabolites.get_by_id(met.id).annotation["pubchem.compound"]
    except KeyError:
        pubchem = "NULL"
    try:
        inchi = model.metabolites.get_by_id(met.id).annotation["inchi"]
    except KeyError:
        inchi = "NULL"   
    
    METABOLITES = METABOLITES.append({"METABOLITESID": metID, "NAME": officialName, "Str_NAME": str_name, "COMPARTMENT": compartment, "KEGG": kegg, "PUBCHEM": pubchem, "INCHI": inchi}, 
                                         ignore_index=True)
    return METABOLITES

def addToStoich(metid, rid, coeff, STOICH):
    STOICH = STOICH.append({"REACTIONSID": rid,"METABOLITESID": metid,"VALUE": coeff}, ignore_index=True)
    return STOICH
    
            

# Main script
# import modules
MODELS = pandas.DataFrame(columns = ["MID","NAME"])
MOD_REACT = pandas.DataFrame(columns = ["MID","RID"])
REACTIONS = pandas.DataFrame(columns = ["RID","NAME","ec-code"])
METABOLITES = pandas.DataFrame(columns = ["METABOLITESID", "NAME", "Str_Name", "COMPARTMENT","KEGG","PUBCHEM","INCHI"])
STOICH = pandas.DataFrame(columns = ["REACTIONSID","METABOLITESID","VALUE"])

# Dictionary to store met IDs
metDict = {}

# Dictionary to store model IDs
modDict = {}

# Dictionary to store rxn IDs
rxnDict = {}

# Dictionary to store Stoich info
stoichDict = {}

# connect to the database 
#cursor = connect()
# read each model in the Agora file 
model_files = loadingAgora("C:\\Users\\jrodi\\OneDrive\\Desktop\\sbml\\")

# Initialize ID counters
current_model_id = 0
current_reaction_id = 0
current_metabolite_id = 0

# Parse metnames.db and add to dataframe
NAME = pandas.read_csv(open('NAME.csv', 'r'))

PSEUDONYM = pandas.read_csv(open('PSEUDONYM.csv', 'r'))

# Create the RECIPE tabel 
## Load the basil and M9 media recipes 
M9 = pandas.read_csv(open('KOMODO/KOMODO_M9.csv', 'r'))
basil = pandas.read_csv(open('KOMODO/KOMODO_basil.csv', 'r'))

## add the media ID 
basil['MEDIAID'] = pandas.Series([1] * len(basil))
M9['MEDIAID'] = pandas.Series([2] * len(M9))

## combine into RECIPE table 
RECIPE = pandas.concat([basil,M9], ignore_index=True)
RECIPE.columns = ["SEEDID","NAME","CONCENTRATION","MEDIAID"] ## NAME is in pseudonym, ID is media ID 


IDS = []
for i in RECIPE["SEEDID"]:
    ids = int(NAME[NAME["name"]==i].get("metabolite")) # returns a series object, use get to get value (key=metabolites)
    IDS.append(ids)
RECIPE["METID"]=IDS
RECIPE = RECIPE.drop('SEEDID', axis=1)

currentMetID = 16316

# Iterate through model files
for i in model_files:
    model = cobra.io.read_sbml_model('C:\\Users\\jrodi\\OneDrive\\Desktop\\sbml\\%s'%i) #read model
    print(model)
    # check if model is already in the table. if not, add to the table 
    if model.id not in modDict:
        current_model_id += 1
        MODELS = MODELS.append({"MID": current_model_id ,"NAME": model.id}, ignore_index=True)
        modDict[model.id] = ''
        #print(MODELS)

        # Get reactions in the model 
        for j in model.reactions:         
            # Check if rxn is in the table, add it if not
            if j.id not in rxnDict:
                current_reaction_id += 1
                REACTIONS, MOD_REACT = addToReactions(j, current_model_id, current_reaction_id,REACTIONS, MOD_REACT)
                rxnDict[j.id] = ''

                # get metabolites and coefficients
                for met,coeff in j.metabolites.items():                
                    # Store met name
                    metName = str(met.id).split('__91__')[0]
                    
                    try:
                        officialName = PSEUDONYM[PSEUDONYM["pseudonym"]==metName].get("official").values[0]
                    except:
                        officialName = metName
                    
                    # Check if met is in NAME
                    try:
                        metID = NAME[NAME["name"]==officialName].get("metabolite").values[0]
                        #print(str(metID))
                    # Add to NAME if not
                    except:
                        currentMetID += 1
                        metID = currentMetID
                        #newRow = pandas.DataFrame({"metabolite": metID ,"name": officialName, "source": "Agora", "sourcetype": "Agora"}, ignore_index=True)
                        #NAME = pandas.concat(NAME, newRow)
                        NAME = NAME.append({"metabolite": metID ,"name": officialName, "source": "Agora", "sourcetype": "Agora"}, ignore_index=True)


                    # Create unique key for stoichDict                
                    stoich = str(metID) + str(current_reaction_id) + str(coeff)
                
                    # If already in stoich then must also already be in met table so break out of loop
                    if stoich in stoichDict:
                        break
                    
                    # If not in stoich but met already added, just add stoich entry
                    elif metID in metDict:
                        # Add to STOICH
                        STOICH = addToStoich( metID, current_reaction_id, coeff, STOICH )
                        stoichDict[stoich] = ''
                            
                    # If not in stoich or mets then increment current ID counter and add to both tables    
                    else:
                        # Add to STOICH
                        STOICH = addToStoich( metID, current_reaction_id, coeff, STOICH )
                        stoichDict[stoich] = ''
                        METABOLITES = addToMetabolites(metID, officialName, met, model, METABOLITES)
                        metDict[metID] = officialName
    else:
        break

# Add dataframes as mySQL tables on bioed
engine_txt = open('engine.txt','r').read()
engine = create_engine(engine_txt, echo=False)
NAME.to_sql(con=engine, name='NAME', if_exists='replace')
PSEUDONYM.to_sql(con=engine, name='PSEUDONYM', if_exists='replace')
MODELS.to_sql(con=engine, name='MODELS', if_exists='replace')
MOD_REACT.to_sql(con=engine, name='MOD_REACT', if_exists='replace')
REACTIONS.to_sql(con=engine, name='REACTIONS', if_exists='replace')
METABOLITES.to_sql(con=engine, name='METABOLITES', if_exists='replace')
RECIPE.to_sql(con=engine, name='RECIPE', if_exists='replace')
