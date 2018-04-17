# returnt true if dosnt already exist
def check(ID, DB):
    if ID in DB["NAME"]:
        return False
    else:
        return True
def loadingAgora(directory):
    # get all the model files in the agora folder, hold in a list
    model_files = os.listdir(directory)[0:5]
    return model_files
def getReactions(reaction, model, REACTIONS, MOD_REACT):
    name = reaction.id
    str_name = reaction.name
    try:
        ec = reaction.annotation['ec-code']
    except KeyError:
        ec = 'NA'
    REACTIONS = REACTIONS.append({ "NAME": name, "Str_NAME": str_name, "ec-code": ec}, ignore_index=True)
    MOD_REACT = MOD_REACT.append( { "MOD_NAME": model, "REACT_NAME": name }, ignore_index=True)
    return REACTIONS, MOD_REACT
def getMetabolites(met, METABOLITES): 
    name = str(met.id).split('__91__')[0]
    str_name = met.name
    compartment = met.compartment 
    if check(name,METABOLITES):
        METABOLITES = METABOLITES.append({"NAME": name,"Str_NAME": str_name,"COMPARTMENT": compartment}, ignore_index=True)
    return METABOLITES
def main():
    # import modules
    import os
    import os.path
    import cobra
    import pandas 
    MODELS = pandas.DataFrame(columns = ["NAME"])
    MOD_REACT = pandas.DataFrame(columns = ["MOD_NAME","REACT_NAME"])
    REACTIONS = pandas.DataFrame(columns = ["NAME","ec-code"])
    METABOLITES = pandas.DataFrame(columns = ["NAME","Str_Name","COMPARTMENT"])
    # connect to the database 
    #cursor = connect()
    
    # read each model in the Agora file 
    model_files = loadingAgora("Agora-1.02/sbml")
    
    # read each model and get the ID
    for i in model_files:
        model = cobra.io.read_sbml_model('Agora-1.02/sbml/%s'%i) #read model
        print(model)
        
        # check if model is already in the database. if not, add to database 
        if check(model.id, MODELS):
            print(check(model.id, MODELS))
            MODELS = MODELS.append({"NAME": model.id}, ignore_index=True)
            
            # Get reactions in the model 
            for j in model.reactions:
                if check(j.id, REACTIONS):
                    REACTIONS, MOD_REACT = getReactions(j, model.id, REACTIONS, MOD_REACT)
                    
                    # get metabolites
                    for k in j.metabolites:
                        if check(str(k.id).split('__91__')[0], METABOLITES ):
                            METABOLITES = getMetabolites(k, METABOLITES)
        else:
            break
    print(MODELS)
    print(REACTIONS)
    print(METABOLITES)
    print(MOD_REACT)
if __name__ == '__main__': main()
