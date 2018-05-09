#!/usr/bin/python3
import pymysql
import sys
import cgi
import cgitb
import os
os.environ[ 'HOME' ] = '/home/students_18/GroupB/cgi-bin/'
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, mpld3
import pandas 
import numpy as np
cgitb.enable()

# print content-type
print("Content-Type:text/html\n")

#get the form
form = cgi.FieldStorage()
modelStatistics = form.getvalue("modelStatistics")
upload = form.getvalue("upload")
#model = form.getvalue("model")
#media = form.getvalue("media")

def printHead():
	print("""
	<html>
	<head>
		<title>COMETS Database</title>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/smoothness/jquery-ui.css">
		<script src="//code.jquery.com/jquery-1.12.4.js"></script>
		<script src="//code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css">

		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script>

		<script>
			$(function() {
				var input = document.getElementById("model");
				
				$( "#model" ).autocomplete({
					source: function(request, response) {
						$.ajax({
							type: "POST",
							url: "autocomplete.py",
							data: JSON.stringify({'input' : input.value}),
							datatype: "application/json",
							success: function(data) {
								response(data)
							}
						});
					},
				});
			})
			$(function() {
				var input = document.getElementById("reactions");
				
				$( "#reactions" ).autocomplete({
					source: function(request, response) {
						$.ajax({
							type: "POST",
							url: "autocompleteRXNS.py",
							data: JSON.stringify({'input' : input.value}),
							datatype: "application/json",
							success: function(data) {
								response(data)
							}
						});
					},
				});
			})
			$(function() {
				var input = document.getElementById("metabolites");
				
				$( "#metabolites" ).autocomplete({
					source: function(request, response) {
						$.ajax({
							type: "POST",
							url: "autocompleteMets.py",
							data: JSON.stringify({'input' : input.value}),
							datatype: "application/json",
							success: function(data) {
								response(data)
							}
						});
					},
				});
			})
		</script>

		<script>
		    function addItem(){
		        var li = document.createElement("LI");  
		        var input = document.getElementById("model");
		        var models = document.getElementById("models");
		        
		        if (models != null){
				    models.value = input.value + ", " + models.value
				}
		        else {
		        	models.value = input.value
		        }

		        li.innerHTML = input.value;
		        li.classList.add("list-group-item");
		        input.value = "";

		        document.getElementById("selectedModels").appendChild(li);
		    }
		    function addRxn(){
		        var li = document.createElement("LI");  
		        var input = document.getElementById("reactions");
		        var rxns = document.getElementById("rxns");
		        
		        if (rxns != null){
				    rxns.value = input.value + ", " + rxns.value
				}
		        else {
		        	rxns.value = rxns.value
		        }

		        li.innerHTML = input.value;
		        li.classList.add("list-group-item");
		        input.value = "";

		        document.getElementById("selectedReactions").appendChild(li);
		    }
		    function addMet(){
		        var li = document.createElement("LI");  
		        var input = document.getElementById("metabolites");
		        var mets = document.getElementById("mets");
		        
		        if (mets != null){
				    mets.value = input.value + ", " + mets.value
				}
		        else {
		        	mets.value = mets.value
		        }

		        li.innerHTML = input.value;
		        li.classList.add("list-group-item");
		        input.value = "";

		        document.getElementById("selectedMets").appendChild(li);
		    }
		</script>

		<style>
			.footer {
				position: fixed;
				left: 0;
				bottom: 0;
				width: 100%;
				background-color: red;
				color: white;
				text-align: center;
			}
		</style>
	</head>""")

def printHomepage():
	print("""
	<body>
		<div class="jumbotron text-center">
			<h1>COMETS Database</h1>
			<p>Virtual experiments using COMETS!</p>
		</div>

		<div class="container" style="margin-bottom: 72.379">
			<ul class="nav nav-tabs" id="myTab" role="tablist">
				<li class="nav-item">
					<a class="nav-link active" id="basic-tab" data-toggle="tab" href="#basic" role="tab" aria-controls="basic" aria-selected="true">Basic</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" id="advanced-tab" data-toggle="tab" href="#advanced" role="tab" aria-controls="advanced" aria-selected="false">Advanced</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" id="visualizations-tab" data-toggle="tab" href="#visualizations" role="tab" aria-controls="visualizations" aria-selected="false">Visualizations</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" id="statistics-tab" data-toggle="tab" href="#statistics" role="tab" aria-controls="statistics" aria-selected="false">Statistics</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" id="about-tab" data-toggle="tab" href="#about" role="tab" aria-controls="about" aria-selected="false">About</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" id="help-tab" data-toggle="tab" href="#help" role="tab" aria-controls="help" aria-selected="false">Help</a>
				</li>
			</ul>

			<div class="tab-content">""")
	printBasic()
	printAdvanced()
	printVisualizations()
	printStatistics()
	printAbout()
	printHelp()

def printBasic():
	print("""
		<div id="basic" class="tab-pane active" role="tabpanel" aria-labelledby="basic-tab">
		    <form id="myForm" name="myForm" action="LayoutGeneration.py" method="POST" enctype="multipart/form-data" target="_blank">
		    	<div class="container-fluid" style="padding-top: 15px;">
					<div class="row flex-row">
						<div class="col-md-6">
							<div class="col-10">
								<h2>Select Model and Media</h2>

								<div class="form-group">

								    <label for="model">Model</label>

								    <input id="model" class="form-control" type="text" name="model" placeholder="Choose Models" value="">

								    <input type="hidden" id="models" name="models" value="">

								    <div style="padding-top: 20px;">
								    	<input type="button" class="btn btn-secondary" id="btnAdd" value="Add Model" onclick="addItem()">
								    	<input type="button" class="btn btn-secondary" value="Clear Models" onClick="window.location.reload()">
								    	<a href="https://bioed.bu.edu/cgi-bin/students_18/GroupB/printAllModels.py" class="btn btn-secondary" target="_blank">View All Models</a>
								    </div>

								    <br>

								    <label for="media">Media</label>

								    <select id="media" name="media" class="form-control" form="myForm">
								    	<option value="">Choose Media</option>
										<option value="Basal">Basal</option>
										<option value="M9">M9</option>
									</select>
								</div>
								<input type="submit" class="btn btn-success" value="Submit">
							</div>
							<div class="col-2">
							</div>
						</div>
						<div class="col-md-6">
							<h2>Selected Models:</h2>
							<ul id="selectedModels" name="selectedModels" class="list-group">

							</ul>
						</div>
				
					</div>
				</div>
			</form>
		</div>""")

def printAdvanced():
	print("""
		<div id="advanced" class="tab-pane" role="tabpanel" aria-labelledby="advanced-tab">
		    <div class="row" style="padding-top: 15px;">
				<h2>Advanced Search</h2>
			</div>
			<form id="advForm" name="advForm" action="AdvancedLayoutGeneration.py" method="POST" enctype="multipart/form-data" target="_blank">
		    	<div class="container-fluid" style="padding-top: 15px;">
					<div class="row flex-row">
						<div class="col-md-6">
							<div class="col-10">
								<div class="form-group">

								    <label for="model">Reactions</label>

								    <input id="reactions" class="form-control" type="text" name="reactions" placeholder="Choose Reactions" value="">

								    <input type="hidden" id="rxns" name="rxns" value="">

								    <div style="padding-top: 20px;">
								    	<input type="button" class="btn btn-secondary" id="btnAdd" value="Add Reaction" onclick="addRxn()">
								    	<input type="button" class="btn btn-secondary" value="Clear Selected" onClick="window.location.reload()">
								    </div>

								    <div style="padding-top: 10px;">
								    	<a href="https://bioed.bu.edu/cgi-bin/students_18/GroupB/printAllRxns.py" class="btn btn-secondary" target="_blank">View All Reactions</a>
								    </div>

								    <br>

								    <label for="model">Metabolites</label>

								    <input id="metabolites" class="form-control" type="text" name="metabolites" placeholder="Choose Metabolites" value="">

								    <input type="hidden" id="mets" name="mets" value="">

								    <div style="padding-top: 20px;">
								    	<input type="button" class="btn btn-secondary" id="btnAdd" value="Add Metabolite" onclick="addMet()">
								    	<input type="button" class="btn btn-secondary" value="Clear Selected" onClick="window.location.reload()">
								    </div>

								    <div style="padding-top: 10px;">
								    	<a href="https://bioed.bu.edu/cgi-bin/students_18/GroupB/printAllMets.py" class="btn btn-secondary" target="_blank">View All Metabolites</a>
								    </div>

								    <br>
								    
								</div>
								<input type="submit" class="btn btn-success" value="Submit">
							</div>
							<div class="col-2">
							</div>
						
						</div>
						<div class="col-md-6">
							<h2>Selected Reactions:</h2>
							<ul id="selectedReactions" name="selectedReactions" class="list-group">

							</ul>

							<br>

							<h2>Selected Metabolites:</h2>
							<ul id="selectedMets" name="selectedMets" class="list-group">

							</ul>
						</div>
					</div>
				</div>
			</form>
	    </div>""")

def printVisualizations():
	print("""
		<div id="visualizations" class="tab-pane" role="tabpanel" aria-labelledby="visualizations-tab">
					<form name="myForm" action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/website.py" method="POST" enctype="multipart/form-data">
						<div class="row" style="padding-top: 15px;">
							<div class = "col-6">
								<h2>Visualizations</h2>
										<br>
										<br>
										<div class="form-group">

											<h4>Upload the total_biomass.txt</h4>
										
											<input type="file" name = "file_upload" size=1000 accept=".txt">
											<input type = "submit" value = "Submit">
										</div>
							</div>	
						</div>	
					</form>
					<p id = "message"></p>
				""")
	file = form.getvalue("file_upload")
	if file:
		read = pandas.read_table(form["file_upload"].file, index_col = 0, sep=("\t"))
		print(loadFile(read))

	print("""
		</div>
	""")

def printStatistics():
	print("""
		
		<div id="statistics" class="tab-pane" role="tabpanel" aria-labelledby="statistics-tab">
			<br />
			<div class="row" style="padding-top: 15px;">
				<h2>Database Statistics</h2>
			</div>
			<br />
			<div class = "row">
		""")
	print(main_stats())

	print("""
			</div>
			<br>
			<br />
			<br />
			<br />
			<br />
			<br />
			<div class = "row">
				<form name="myForm" action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/website.py" method="POST">
					<h2>Search models to see associated reactions and metabolites</h2>
					<br />
					<div class="col-6">
						<div class="form-group">					
					    	<label for = "Models">Models</label>
					    	<input id='modelStatistics' name = 'modelStatistics' class="form-control" type="text" placeholder = "Search model..." value="%s"/>
					   	</div>
					</div>
					<div class="col-1">
					   	<input type="submit" class="btn btn-success" value="Search" >
					</div>
				</form>
			</div>
			"""%(modelStatistics))
	if form: # if form was submitted
		print(modelStat(modelStatistics))
	print("""
			<br />
			<br />
			<br />
			<br />
			<br />
			<br />
			<div>
				<h2>Distribution Of Metabolites Per Model</h2>
				<img src="https://bioed.bu.edu/students_18/GroupB/density.png" />
			</div>
		</div>
		""")

def printAbout():
	print("""
		<div id="about" class="tab-pane" role="tabpanel" aria-labelledby="about-tab">
	    	<div class="row" style="padding-top: 15px;">
				<h2>About</h2>
			</div>
			<div class="row">
				<p>This project was developed at Boston University as part of BF768, Spring 2018, G. Benson 
				instructor. Our website provides a user friendly interface to run virtual experiments using COMETS, and 
				visualize the results. COMETS stands for computation of microbial ecosystems in time and space, 
				and is used to simulate metabolic models. Users can select models, reactions, metabolites, and 
				media to run customized experiments. After the user selects the desired inputs, our site generates 
				a layout file that can be sent to COMETS. The resulting COMETS output can be uploaded in the upload 
				tab of our site and visualizations of the results will be shown. All data provided by the Segre Lab. 
				Website and Database design by Jonathan Rodiger, Maxwell Brown, Andrew Hamel. Boston University 
				department of Bioinformatics. </p>
			</div>
			<div class = "row">
				<p>
				<a href = "http://www.bu.edu/segrelab/comets/">COMETS Segre Lab at Boston University</a>
				</p>
			</div>
			<div class = "row">
				<p>
				<a href = "http://komodo.modelseed.org/">Media Recipes</a>
				</p>
			</div>
	    </div>""")

def printHelp():
	print(""" 
			<div id="help" class="tab-pane" role="tabpanel" aria-labelledby="help-tab">
			    <div class="container-fluid" style="padding-top: 15px;">
					<div class="row flex-row">
						<div class = "col-6">
							<h3>Basic</h3>
								<p>In the basic search, the user will choose the model species and media desired. 
								The user can input more than one model species and only one media.  After typing 
								a model, click Add Model.  The model selected will move to the right side of the page 
								underneath the section Selected Models.  If the user wants to choose more than one model, 
								the previous model must be moved to the Selected Models section first. If the user 
								does not like the models chosen prior to submitting, then the user can press the Clear 
								Models button to start over.  Additionally, the user can click View All Models to scan 
								all of the models within the database. 
								Next, the user will input one media: either Basal or M9.
								After model species and media are chosen, the user will click submit to generate a layout file. 
								The layout file will be moved to a new screen. The user can save the page for later use. Below is 
								a partial image of a generated layout file. 
								</p>
							<h3>Advanced</h3>
								<p>The advanced search is used if the user would like to determine what model species are contain any 
								desired reactions, metabolites, and or media.  Similarly with the basic search, the user will input 
								any reactions the user chooses and press the \"Add Reactions\" button. This will be repeated for 
								metabolites. A media will be chosen as well.  The user will then press submit and the user will be 
								shown what model species satisfy those conditions. The model species can then be chosen in the basic 
								search. 
								</p>
							<h3>Visualization: Load Data</h3>
								<p> 
								After COMETS runs a simulation, files are returned to the user including a total_bimass.txt text file. 
								This file can be uploaded to the website via the visualization tab. When the upload button is selected, 
								the website will prompt the user to select the total_biomass.txt file from the user\'s computer. After 
								submitting the text file, two graphs will print to the screen below the input button. The first graph 
								shows the change in biomass over time. If multiple colonies of the same species are present, the graph 
								plots the average biomass over time.The second graph Shows the rate change of biomass over time.
								</p>
							<h3>Statistics</h3>
								<p>The statistics tab provides simple statistics about the database or a particular model. At the top of 
								the page are simple explanatory statistics about the the database as a whole. This table shows the amount 
								of Models, Metabolites, Reactions, Medias, Kegg IDs, Pubchem IDs, International Chemical Identifier (inchi) 
								in the database. The second portion of the page is a section where the user can look up a specific model 
								and see the number of Reactions, and internal and external metabolites associated with it. The third portion
								of the tab is summary statistics about the the distribution of properties in the database. 
								</p>
							<h3>Layout File</h3>
								<p>Layout File:
									There are several parameters within the layout file. The model_file will denote what model species were chosen. 
									Model_world contains the media conditions.  The metabolites for the model with their CPD identity and concentration 
									are shown. The diffusion constant is set to the default parameter. Media_Refresh is how often the media are fed. They are 
									set to zero.  Static_Media indicates which metabolites should be kept constant. All are set to zero. Initial_Population 
									denotes the initial population for the model species. The parameters are set to the default value. 

								</p>
						</div>
						<div class = "col-6">
							<img src="https://bioed.bu.edu/images/students_18/GroupB/image1.png" class = "img-fluid"/>
							<img src="https://bioed.bu.edu/images/students_18/GroupB/image2.png" class = "img-fluid"/>
							<img src="https://bioed.bu.edu/images/students_18/GroupB/image4.png" class = "img-fluid"/>
							<img src="https://bioed.bu.edu/images/students_18/GroupB/visual.png" class = "img-fluid"/>
							<img src="https://bioed.bu.edu/images/students_18/GroupB/image3.png" class = "img-fluid"/>
						</div>

						""")
	print("""
						</div>
					</div>
				</div>
			</div>
			<div class="row">
				<div class="footer">
					<a href = "http://www.bu.edu/"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Boston_University_wordmark.svg/1280px-Boston_University_wordmark.svg.png" width=160 hight=72.379 ismap></a>
				</div>
			</div>
			<script>
				$('#myTab a').on('click', function (e) {
					e.preventDefault()
					$(this).tab('show')
				})

				$('a[data-toggle="tab"]').on("shown.bs.tab", function (e) {
				    var id = $(e.target).attr("href");
				    localStorage.setItem('selectedTab', id)
				});

				var selectedTab = localStorage.getItem('selectedTab');
				if (selectedTab != null) {
				    $('#myTab a[href="' + selectedTab + '"]').tab('show')
				}
			</script>
		</body>
		</html>""")

def submit_MODEL(model,media):
	query = ""
	if model is not None:
		m = model.split(',')
		query = """SELECT MODEL.name, MEDIA.name FROM MODEL JOIN MEDIA WHERE MEDIA.name = "%s" AND MODEL.name LIKE """%(media)
		query += "\"" + m[0] + "\""
		if m > 1:
			for j in m[1:]:
				query += " AND MODEL.name LIKE \"" + j + "\""

	return query


def execute_query(query):
	with open('login.txt') as f:
		lines=f.readlines()
		username=lines[0].strip()
		password=lines[1].strip()

	# connect to the database
	connection = pymysql.connect(host="bioed.bu.edu",db="groupB",user=username,passwd=password)

	# get cursor
	cursor = connection.cursor()

	# run query
	cursor.execute(query)

	# fetch results 
	results = cursor.fetchall()

	# close the connection
	cursor.close()
	connection.close()

	# return the results
	return results

def graph():
	totalBiomass = pandas.read_table("total_biomass.txt", index_col = 0)
	fig, (ax,bx) = plt.subplots(2)

	# plot growth as ax
	y = totalBiomass.mean(axis=1)
	x = list(range(len(y))) 
	ax.set(xlabel="Time (t)", ylabel='Biomass f(t)',
	       title='Biomass Over Time')
	ax.grid()
	ax.plot(x,y)

	# plot the rate of growth
	rate = np.gradient(np.asarray(y)) # get the rate 
	bx.set(xlabel="Time (t)", ylabel='Biomass f\'(t)',
	       title='Growth Rate')
	bx.grid()
	bx.plot(x,rate)
	plt.subplots_adjust(hspace=.5,
                    wspace=1 )
	
	#print(fig) # figure dimensions 
	print(mpld3.fig_to_html(fig))
#def a finction to create tables in html 
def html_table(headers,output):
    #start table
        #make header
    head = """
        <table id="mainStats" class="table">
        <thead>
        <tr>"""
    for i in headers:
        head+="""<th>%s</th>"""%i
    head+="</tr></thead>"
        #make rows
        #x = row counter
    row="<tbody><tr>"
    for i in output:
        row += """<td>%s</td>"""%(i)        
    row+="""</tr>"""
    #concatinate stings
    table = head + row + """</tbody></table>"""
    return table

#create a query with all the genes 
def main_stats():
    stats = ["MODELS", "METABOLITES", "REACTIONS", "MEDIA"]
    mets = ["KEGG", "PUBCHEM", "INCHI"]
    header = ["MODELS", "METABOLITES", "REACTIONS", "MEDIA", "KEGG", "PUBCHEM", "INCHI"]
    output = []
    for i  in stats:
        query = """select count(*) from %s"""%(i)
        output.extend(execute_query(query)[0])# use extend becasue is a tuple 
    for i in mets:
    	query = """select count(*) from METABOLITES where %s != 'NULL'; """%(i)
    	output.extend(execute_query(query)[0])
    return(html_table(header,output))

def modelStat(model):
    output = [model]
    #reactions
    reactionsQuery = """
    select count(distinct RID)
    from MODELS join MOD_REACT using (MID)
    where NAME LIKE "%s";
    """%(model)
    #metabolites
    metabolitesQuery = """
    select count(distinct METABOLITESID)
    from MODELS join MOD_REACT using (MID)
    join REACTIONS using (RID)
    join STOICH on REACTIONS.RID = STOICH.REACTIONSID
    join METABOLITES using (METABOLITESID)
    where MODELS.NAME LIKE "%s";
    """%(model)
    extmetabolitesQuery = """
    select count(distinct METABOLITESID)
    from MODELS join MOD_REACT using (MID)
    join REACTIONS using (RID)
    join STOICH on REACTIONS.RID = STOICH.REACTIONSID
    join METABOLITES using (METABOLITESID)
    where MODELS.NAME LIKE "%s" and COMPARTMENT = "c";
    """%(model)
    intmetabolitesQuery = """
    select count(distinct METABOLITESID)
    from MODELS join MOD_REACT using (MID)
    join REACTIONS using (RID)
    join STOICH on REACTIONS.RID = STOICH.REACTIONSID
    join METABOLITES using (METABOLITESID)
    where MODELS.NAME LIKE "%s" and COMPARTMENT = "e";
    """%(model)
    output.extend(execute_query(reactionsQuery)[0])
    output.extend(execute_query(metabolitesQuery)[0])
    output.extend(execute_query(extmetabolitesQuery)[0])
    output.extend(execute_query(intmetabolitesQuery)[0])
    header = ["Model","Reactions", "Total Metabolites", "Internal Metabolites", "External Metabolites"]
    table =html_table(header,output)
    return table

def loadFile(total_biomass):
	fig, (ax,bx) = plt.subplots(2)

	y = total_biomass.mean(axis=1)
	x = list(range(len(y))) 
	ax.set(xlabel="Time (t)", ylabel='Biomass f(t)',
		title='Biomass Over Time')
	ax.grid()
	ax.plot(x,y)

	# plot the rate of growth
	rate = np.gradient(np.asarray(y)) # get the rate 
	bx.set(xlabel="Time (t)", ylabel='Biomass f\'(t)',
		title='Growth Rate')
	bx.grid()
	bx.plot(x,rate)
	plt.subplots_adjust(hspace=.5, wspace=1 )
	
	#print(fig) # figure dimensions 
	print(mpld3.fig_to_html(fig))

#query = submit_MODEL(model,media)
#print(execute_query(query))

printHead()
printHomepage()