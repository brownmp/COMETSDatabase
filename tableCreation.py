import os
import os.path
import cobra
import pandas
import pymysql
import cgi
import cgitb
import pymysql
cgitb.enable()

# Methods
# connect to the mySQL database and return the cursor and connection 
def connect(username,password, database, host): 
    connection = pymysql.connect(host=host, db = database, user=username, passwd=password)
    cursor = connection.cursor()
    return cursor, connection

def insert_model():
    connection = pymysql.connect()
    cursor = connection.cursor()
    query = "INSERT INTO MODEL (NAME) VALUES("
    for i in MODELS["NAME"]:
        query += '"' + i + '"'+"),("
    query = query[0:-2]
    query += ";"
    cursor.execute(query)
    connection.commit()
    
def insert_reactions():
    connection = pymysql.connect()
    cursor = connection.cursor()
    query = "INSERT INTO REACTIONS (NAME, EC) VALUES("
    for index, row in REACTIONS.iterrows():
        query += '"' + row["NAME"] + '"'+"," + '"' + row["ec-code"] + '"'+"),("
    query = query[0:-2]
    query += ";"
    cursor.execute(query)
    connection.commit()

def insert_metabolites():
    connection = pymysql.connect()
    cursor = connection.cursor()
    query = "INSERT INTO METABOLITES (NAME, STRING_NAME) VALUES("
    for index, row in METABOLITES.iterrows():
        query += '"' + row["NAME"] + '"'+"," + '"' + row["Str_NAME"] + '"'+"),("
    query = query[0:-2]
    query += ";"
    cursor.execute(query)
    connection.commit()
    
def loadingAgora(directory):
    # get all the model files in the agora folder, hold in a list
    model_files = os.listdir(directory)[0:2]
    return model_files

def addToReactions(reaction, model, current_reaction_id, REACTIONS, MOD_REACT):
    name = reaction.id
    str_name = reaction.name
    try:
        ec = reaction.annotation['ec-code']
    except KeyError:
        ec = 'NA'    
    REACTIONS = REACTIONS.append({"RID": current_reaction_id ,"NAME": name, "Str_NAME": str_name, "ec-code": ec}, ignore_index=True)
    MOD_REACT = MOD_REACT.append( { "MOD_NAME": model, "REACT_NAME": name }, ignore_index=True)
    return REACTIONS, MOD_REACT

def addToMetabolites(metid, met, model, METABOLITES): 
    name = str(met.id).split('__91__')[0]
    str_name = met.name
    compartment = met.compartment 
    
    try:
        kegg = model.metabolites.get_by_id(met.id).annotation["kegg.compound"]
    except KeyError:
        kegg = 'NA'
    try:
        pubchem = model.metabolites.get_by_id(met.id).annotation["pubchem.compound"]
    except KeyError:
        pubchem = 'NA'
    try:
        inchi = model.metabolites.get_by_id(met.id).annotation["inchi"]
    except KeyError:
        inchi = 'NA'
    
    if notInTable(name,METABOLITES):
        METABOLITES = METABOLITES.append({"METABOLITESID":metid, "NAME": name,"Str_NAME": str_name,"COMPARTMENT": compartment, "KEGG": kegg, "PUBCHEM": pubchem, "INCHI": inchi}, 
                                         ignore_index=True)
    return METABOLITES

def addToStoich(metid, rid, coeff, STOICH):
    STOICH = STOICH.append({"REACTIONSID": rid,"METABOLITESID": metid,"VALUE": coeff}, ignore_index=True)
    return STOICH


# Main script
# import modules
MODELS = pandas.DataFrame(columns = ["MID","NAME"])
MOD_REACT = pandas.DataFrame(columns = ["MOD_NAME","REACT_NAME"])
REACTIONS = pandas.DataFrame(columns = ["RID","NAME","ec-code"])
METABOLITES = pandas.DataFrame(columns = ["METABOLITESID", "NAME","Str_Name","COMPARTMENT","KEGG","PUBCHEM","INCHI"])
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

# Iterate through model files
for i in model_files:
    model = cobra.io.read_sbml_model('C:\\Users\\jrodi\\OneDrive\\Desktop\\sbml\\%s'%i) #read model
    print(model)
    # check if model is already in the table. if not, add to the table 
    if model.id not in modDict:
        current_model_id += 1
        MODELS = MODELS.append({"MID": current_model_id ,"NAME": model.id}, ignore_index=True)
        modDict[model.id] = ''
        print(MODELS)
               
        # Get reactions in the model 
        for j in model.reactions:         
            # Check if rxn is in the table, add it if not
            if j.id not in rxnDict:
                current_reaction_id += 1
                REACTIONS, MOD_REACT = addToReactions(j, model.id, current_reaction_id,REACTIONS, MOD_REACT)
                rxnDict[j.id] = ''

                # get metabolites and coefficients
                for met,coeff in j.metabolites.items():                
                    # Store met name
                    metID = str(met.id).split('__91__')[0]
                    
                    # Create unique key for stoichDict                
                    stoich = metID + str(current_reaction_id) + str(coeff)
                
                    # If already in stoich then must also already be in met table so break out of loop
                    if stoich in stoichDict:
                        break
                    
                    # If not in stoich but met already added, just add stoich entry and lookup metID with dict
                    elif metID in metDict:
                        stoichDict[stoich] = ''
                        # Add to STOICH
                        STOICH = addToStoich( metDict[metID], current_reaction_id, coeff, STOICH )
                        
                    # If not in stoich or mets then increment current ID counter and add to both tables    
                    else:
                        current_metabolite_id += 1
                        metDict[metID] = current_metabolite_id
                        METABOLITES = addToMetabolites(current_metabolite_id, met, model, METABOLITES)
                        # Add to STOICH
                        STOICH = addToStoich( current_metabolite_id, current_reaction_id, coeff, STOICH )
                        stoichDict[stoich] = ''
    else:
        break
print(MODELS)
print(REACTIONS)
print(METABOLITES)
print(MOD_REACT)
print(STOICH)