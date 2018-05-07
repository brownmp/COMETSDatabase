import pymysql

def Get_Model_World(models,media):
    model_world = []
    connection = pymysql.connect(host = "bioed.bu.edu", db = "groupB", user = "ahamel19", passwd = "Sparticus6")
    cursor = connection.cursor()
    media_query = """SELECT MEDIAID FROM MEDIA WHERE MEDIA.NAME = '%s'"""%(media)
    cursor.execute(media_query)
    media_query_results = cursor.fetchone()
    concentration_query = """SELECT distinct NAME.name, METABOLITES.COMPARTMENT, RECIPE.CONCENTRATION
    FROM MODELS JOIN MOD_REACT USING(MID) JOIN REACTIONS USING(RID) JOIN STOICH ON REACTIONS.RID = STOICH.REACTIONSID JOIN METABOLITES USING(METABOLITESID) JOIN RECIPE ON (METABOLITES.METABOLITESID = RECIPE.METID) JOIN NAME ON NAME.metabolite = RECIPE.METID
    WHERE NAME.name regexp "^cpd" AND """
    concentration_query += """MODELS.NAME = '%s' """%(models)
    concentration_query += """AND RECIPE.MEDIAID=%i"""%(media_query_results[0])
    cursor.execute(concentration_query)
    concentration_results = cursor.fetchall()
    for i in concentration_results:
        model_world.append("%s_%s0 %s"%(i))
    null_query = """SELECT distinct NAME.name,METABOLITES.COMPARTMENT
    FROM MODELS JOIN MOD_REACT USING(MID) JOIN REACTIONS USING(RID) JOIN STOICH ON REACTIONS.RID = STOICH.REACTIONSID JOIN METABOLITES USING(METABOLITESID) JOIN NAME ON NAME.metabolite = METABOLITES.METABOLITESID
    WHERE MODELS.NAME = '%s' """%(models)
    null_query += """AND NAME.name regexp "^cpd" AND NAME.name NOT IN(SELECT distinct NAME.name
    FROM MODELS JOIN MOD_REACT USING(MID) JOIN REACTIONS USING(RID) JOIN STOICH ON REACTIONS.RID = STOICH.REACTIONSID JOIN METABOLITES USING(METABOLITESID) JOIN RECIPE ON (METABOLITES.METABOLITESID = RECIPE.METID) JOIN NAME ON NAME.metabolite = RECIPE.METID
    WHERE MODELS.NAME = '%s' """%(models)
    null_query += """AND NAME.name regexp '^cpd' AND RECIPE.MEDIAID=%i """%(media_query_results[0])
    null_query += """)"""
    cursor.execute(null_query)
    null_results = cursor.fetchall()
    for i in null_results:
        model_world.append("%s_%s0 0"%i)
    return model_world


def get_LayoutFile(models,media):
    layout_file = ""
    model_file = []
    model_file.append(models)
    lst = []
    #create model_file
    for i in model_file:
        lst.append(i+"_xml.txt ")
    t = ''.join(lst)
    v = "model_file",t
    lt = map(str,v)
    line = " ".join(lt)
    
    #write model_file to layout file
    #layout = open("layout.txt","w")
    #layout.write(line+"\n")
    layout_file += line+"\n"
    
    #create model_world
    
    #layout.write("\tmodel_world\n\t\tgrid_size 1 1\n\t\tworld_media\n")
    layout_file += "\tmodel_world\n\t\tgrid_size 1 1\n\t\tworld_media\n"
    
    y = Get_Model_World(models,media)
    for i in y:
        #layout.write("\t\t"+i+"\n")
        layout_file += "\t\t"+i+"\n"

    #diffusion_constants
    #layout.write("\t//")
    layout_file += "\t//"
    #layout.write("\n\tdiffusion_constants 1.000000e-06\n")
    layout_file += "\n\tdiffusion_constants 1.000000e-06\n"
    
    diff = []
    for j in range(len(y)):
        diff.append("%i 0"%(j+1))

    for k in range(len(diff)):
        #layout.write("\t\t" + diff[k]+"\n") 
        layout_file += "\t\t" + diff[k]+"\n"
    
    #media
    #layout.write("\n\t//\n\tmedia\n\t//")
    layout_file += "\n\t//\n\tmedia\n\t//"
    
    #media_refresh
    #layout.write("\n\tmedia_refresh ")
    layout_file += "\n\tmedia_refresh "
    
    g = ["0"]*len(diff)
    #layout.write(",".join(g).replace(","," "))
    layout_file += ",".join(g).replace(","," ")

    #static_media
   # layout.write("\n\t//\n\t")
    layout_file += "\n\t//\n\t"
    
    #layout.write("static_media")
    layout_file += "static_media"
    
    h = ["0"]*len(diff)*2
    #layout.write(",".join(h).replace(","," "))
    layout_file += ",".join(h).replace(","," ")
    
    #layout.write("\n\t//\n\tbarrier\n\t//\n//")
    layout_file += "\n\t//\n\tbarrier\n\t//\n//"
    
    #write intitial population
    #layout.write("\ninitial_pop\n")
    layout_file += "\ninitial_pop\n"
    
    #layout.write("\t")
    layout_file += "\t"
    
    #layout.write("0 0 1.000000e-09 1.000000e-09")
    layout_file += "0 0 1.000000e-09 1.000000e-09"
    
    #layout.write("\n//")
    layout_file += "\n//"
    
    #write parameters to layout file
    layout.write("\n")
    #layout_file += "\n"
    
    
    
    layout_file += """\tparameters
\tmaxCycles = 500
\tpixelScale = 5
\tsaveslideshow = false
\tslideshowExt = png
\tslideshowColorRelative = true
\tslideshowRate = 1
\tslideshowLayer = 324
\twriteFluxLog = true
\tFluxLogName = flux.m
\tFluxLogRate = 1
\twriteMediaLog = false
\tMediaLogName = ./media.txt
\tMediaLogRate = 1
\twriteBiomassLog = false
\tBiomassLogName = ./biomass.txt
\tBiomassLogRate = 1
\twriteTotalBiomassLog = true
\ttotalBiomassLogRate = 1
\tTotalbiomassLogName = ./total_biomass
\tuseLogNameTimeStamp = false
\tslideshowName = ./res.png
\tnumDiffPerStep = 10
\tnumRunThreads = 1
\tgrowthDiffRate = 0
\tflowDiffRate = 3e-09
\texchangestyle = Monod Style
\tdefaultKm = 0.01
\tdefaultHill = 1
\ttimeStep = 0.1
\tdeathRate = 0
\tspaceWidth = 0.01
\tmaxSpaceBiomass = 1
\tminSpaceBiomass = 0
\tallowCellOverlap = true
\ttoroidalWorld = false
\tshowCycleTime = true
\tshowCycleCount = true
\tdefaultVmax = 10
\tbiomassMotionStyle = Diffusion (Crank-Nicolson)
\texchangeStyle = Standard FBA"""
    
    #layout.write("\n//")
    layout_file += "\n//"
    
    #layout.close()
    
    return layout_file

u = get_LayoutFile("Ruminococcus_torques_ATCC_27756","Basal")
print(u)