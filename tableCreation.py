# returnt true if dosnt already exist
import os
import os.path
import cobra
import pandas
import pymysql
import cgi
import cgitb
cgitb.enable()

# Methods
def insert_model():
    connection = pymysql.connect(host="bioed.bu.edu",db = "groupB",user = "ahamel19",passwd = "Sparticus6")
    cursor = connection.cursor()
    query = "INSERT INTO MODEL (NAME) VALUES("
    for i in MODELS["NAME"]:
        query += i + "),"
    query = query[0:-2]
    query += ";"
    print(query)
    
def insert_reactions():
    connection = pymysql.connect(host="bioed.bu.edu",db = "groupB",user = "ahamel19",passwd = "Sparticus6")
    cursor = connection.cursor()
    query = "INSERT INTO REACTIONS (NAME, EC) VALUES("
    for index, row in REACTIONS.iterrows():
        query += row["NAME"] + "," + row["ec-code"] + "),("
    query = query[0:-2]
    query += ";"
    print(query)

def insert_metabolites():
    connection = pymysql.connect(host="bioed.bu.edu",db = "groupB",user = "ahamel19",passwd = "Sparticus6")
    cursor = connection.cursor()
    query = "INSERT INTO METABOLITES (NAME, STRING_NAME) VALUES("
    for index, row in METABOLITES.iterrows():
        query += row["NAME"] + "," + row["Str_NAME"] + "),("
    query = query[0:-2]
    query += ";"
    print(query)
 
def check(ID, DB):
    if ID in DB["NAME"]:
        return False
    else:
        return True
    
def loadingAgora(directory):
    # get all the model files in the agora folder, hold in a list
    model_files = os.listdir(directory)[0:3]
    return model_files

def getReactions(reaction, model, current_reaction_id, REACTIONS, MOD_REACT):
    name = reaction.id
    str_name = reaction.name
    try:
        ec = reaction.annotation['ec-code']
    except KeyError:
        ec = 'NA'
    REACTIONS = REACTIONS.append({"RID": current_reaction_id ,"NAME": name, "Str_NAME": str_name, "ec-code": ec}, ignore_index=True)
    MOD_REACT = MOD_REACT.append( { "MOD_NAME": model, "REACT_NAME": name }, ignore_index=True)
    return REACTIONS, MOD_REACT

def getMetabolites(met, METABOLITES): 
    name = str(met.id).split('__91__')[0]
    str_name = met.name
    compartment = met.compartment 
    if check(name,METABOLITES):
        METABOLITES = METABOLITES.append({"NAME": name,"Str_NAME": str_name,"COMPARTMENT": compartment}, 
                                         ignore_index=True)
    return METABOLITES

def getStoich(met, reaction, coeff, STOICH):
    rid = reaction.id
    metid = str(met.id).split('__91__')[0]
    value = coeff
    STOICH = STOICH.append({"REACTIONSID": rid,"METABOLITESID": metid,"VALUE": coeff}, ignore_index=True)
    return STOICH

# Main script
# import modules
MODELS = pandas.DataFrame(columns = ["MID","NAME"])
MOD_REACT = pandas.DataFrame(columns = ["MOD_NAME","REACT_NAME"])
REACTIONS = pandas.DataFrame(columns = ["RID","NAME","ec-code"])
METABOLITES = pandas.DataFrame(columns = ["NAME","Str_Name","COMPARTMENT"])
STOICH = pandas.DataFrame(columns = ["REACTIONSID","METABOLITESID","VALUE"])
# connect to the database 
#cursor = connect()
# read each model in the Agora file 
model_files = loadingAgora("/Users/andrewhamel/Desktop/Databases/Project/Agora/sbml/")
current_model_id, current_reaction_id = 0
# read each model and get the ID
for i in model_files:
    model = cobra.io.read_sbml_model('/Users/andrewhamel/Desktop/Databases/Project/Agora/sbml/%s'%i) #read model
    print(model)
    # check if model is already in the database. if not, add to database 
    if check(model.id, MODELS):
        current_model_id += 1
        MODELS = MODELS.append({"MID": current_model_id ,"NAME": model.id}, ignore_index=True)
        # Get reactions in the model 
        for j in model.reactions:
            if check(j.id, REACTIONS):
                current_reaction_id += 1
                REACTIONS, MOD_REACT = getReactions(j, model.id, current_reaction_id,REACTIONS, MOD_REACT)
                # get metabolites and coefficients
                for met,coeff in j.metabolites.items():
                    if check(str(met.id).split('__91__')[0], METABOLITES ):
                        METABOLITES = getMetabolites(met, METABOLITES)
                        STOICH = getStoich(met, j, coeff, STOICH)
    else:
        break
print(MODELS)
print(REACTIONS)
print(METABOLITES)
print(MOD_REACT)
print(STOICH)
