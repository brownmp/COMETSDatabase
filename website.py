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
#model = form.getvalue("model")
#media = form.getvalue("media")

def printHead():
	print("""
	<html>
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/smoothness/jquery-ui.css">
		<script src="//code.jquery.com/jquery-1.12.4.js"></script>
		<script src="//code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css">

		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script>

		<script>
			$( "#model" ).autocomplete({
				
				source: function(request, response) {
					$.ajax({
						type: "POST",
						url: "https://bioed.bu.edu/cgi-bin/students_18/GroupB/autocomplete.py",
						data: "tag_part=" + request.term,
						success: function(data) {
							response(data);
						}
					});
				},
				minLength: 2
			});
		</script>

		<script>
		    function addItem(){
		        var li = document.createElement("LI");  
		        var input = document.getElementById("model");
		        li.innerHTML = input.value;
		        li.classList.add("list-group-item");
		        input.value = "";

		        document.getElementById("selectedModels").appendChild(li);
		    }
		</script>
	</head>
	""")

def printHomepage():
	print("""
	<body>
		<div class="jumbotron text-center">
			<h1>Biological Databases Project</h1>
			<p>Virtual experiments using COMETS!</p>
		</div>

		<div class="container">
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
		    <div class="container-fluid" style="padding-top: 15px;">
				<div class="row flex-row">
					<div class="col-md-6">
						<form name="myForm" action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/Homepage.py" method="POST">
							<div class="col-10">
								<h2>Select Model and Media</h2>

								<div class="form-group">

								    <label for="model">Model</label>

								    

								    <input id="model" class="form-control" type="text" name="model" placeholder="Choose Models">

								    <div style="padding-top: 20px;">
								    	<input type="button" class="btn btn-secondary" id="btnAdd" value="Add Model" onclick="addItem()">
								    	<input type="button" class="btn btn-secondary" value="Clear Models" onClick="window.location.reload()">
								    	<a href="https://bioed.bu.edu/cgi-bin/students_18/GroupB/printAllModels.py" class="btn btn-secondary" target="_blank">View All Models</a>
								    </div>

								    <br>

								    <label for="media">Media</label>

								    <select class="form-control">
								    	<option value="">Choose Media</option>
										<option value="Basal">Basal</option>
										<option value="M9">M9</option>
									</select>
								</div>
								<input type="submit" class="btn btn-success" value="Submit" >
							</div>
							<div class="col-2">
							</div>
						</form>
					</div>
					<div class="col-md-6">
						<h2>Selected Models:</h2>
						<ul id="selectedModels" class="list-group">

						</ul>
					</div>
				</div>
			</div>
		</div>""")

def printAdvanced():
	print("""
		<div id="advanced" class="tab-pane" role="tabpanel" aria-labelledby="advanced-tab">
		    <div class="row" style="padding-top: 15px;">
				<h2>Advanced Search</h2>
			</div>
			<form name="myForm" action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/Advanced.py" method="POST">
				<div class="row">
					<div class="col-md-4">
						<div class="form-group">
						    <label for="media">Media</label>
						    <select class="form-control">
						    	<option value="">Choose Media</option>
								<option value="Basal">Basal</option>
								<option value="M9">M9</option>
							</select>
						</div>
					</div>

					<div class="col-md-4">
						<div class="form-group">
							<label for="reactions">Reactions</label>
							<input id="reactions" class="form-control" type="text" name="reactions" placeholder="Choose Reactions">
						</div>
					</div>

					<div class="col-md-4">
						<div class="form-group">
							<label for="metabolites">Metabolites</label>
							<input id="metabolites" class="form-control" type="text" name="metabolites" placeholder="Choose Metabolites">
						</div>
					</div>
				</div>
				<div class="row">
					<div class="col">
						<input type="submit" class="btn btn-success" value="Submit" >
					</div>
				</div>
			</form>
	    </div>""")

def printVisualizations():
	print("""
		<div id="visualizations" class="tab-pane" role="tabpanel" aria-labelledby="visualizations-tab">
			<div class="row" style="padding-top: 15px;">
				<h2>Visualizations</h2>
			</div>
		""")

	graph()

	print("""
		</div>
		""")

def printStatistics():
	print("""
		<br />
		<div id="statistics" class="tab-pane" role="tabpanel" aria-labelledby="statistics-tab">
		<div class="row" style="padding-top: 15px;">
			<h2>Database Statistics</h2>
		</div>
		<br />
		""")
	print(main_stats())

	print("""
		<br />
		<form name="myForm" action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/website.py" method="POST">
			<h4>Search models to see associated reactions and metabolites</h4>
		<br />
			<div class="col-md-4">
			    <div class="form-group">
			        <label for = "Models">Models</label>
			        <input id='modelStatistics' name = 'modelStatistics' class="form-control" type="text" placeholder = "Search model..." value="%s"/>
			    </div>
			</div>
			<div class="row">
			    <div class="col">
			        <input type="submit" class="btn btn-success" value="Search" >
			    </div>
			</div>
		</form>
		<br />
		"""%(modelStatistics))
	if form: # if form was submitted
		print(modelStat(modelStatistics))
	
	print("""
		</div>
		""")

def printAbout():
	print("""
		<div id="about" class="tab-pane" role="tabpanel" aria-labelledby="about-tab">
	    	<div class="row" style="padding-top: 15px;">
				<h2>About</h2>
			</div>
			<div class="row">
				<p>Our website provides a user friendly interface to run virtual experiments using COMETS, and 
				visualize the results. COMETS stands for computation of microbial ecosystems in time and space, 
				and is used to simulate metabolic models. Users can select models, reactions, metabolites, and 
				media to run customized experiments. After the user selects the desired inputs, our site generates 
				a layout file that can be sent to COMETS. The resulting COMETS output can be uploaded in the upload 
				tab of our site and visualizations of the results will be shown. All data provided by the Segre Lab. 
				Website and Database design by Jonathan Rodiger, Maxwell Brown, Andrew Hamel. Boston University 
				department of Bioinformatics. </p>
			</div>
	    </div>""")

def printHelp():
	print(""" 
			<div id="help" class="tab-pane" role="tabpanel" aria-labelledby="help-tab">
			    <div class="container-fluid" style="padding-top: 15px;">
					<div class="row flex-row">
						<div class="col-md-6">
							<form name="myForm" action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/Homepage.py" method="POST">
								<div class="col-10">
									<h2>Select Model and Media</h2>

									<div class="form-group">

									    <label for="model">Model</label>

									    

									    <input id="model" class="form-control" type="text" name="model" placeholder="Choose Models">

									    <div style="padding-top: 20px;">
									    	<input type="button" class="btn btn-secondary" id="btnAdd" value="Add Model" onclick="addItem()">
									    	<input type="button" class="btn btn-secondary" value="Clear Models" onClick="window.location.reload()">
									    </div>

									    <br>

									    <label for="media">Media</label>

									    <select class="form-control">
									    	<option value="">Choose Media</option>
											<option value="Basal">Basal</option>
											<option value="M9">M9</option>
										</select>
									</div>
									<input type="submit" class="btn btn-success" value="Submit" >
								</div>
								<div class="col-2">
								</div>
							</form>
						</div>
						<div class="col-md-6">
							<div class="row" style="padding-top: 15px;">
								<h2>Results Visualizations</h2>
							</div>""")
	graph()
	print("""
						</div>
					</div>
				</div>
			</div>
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
    for i  in mets:
        query = """select count(*) from METABOLITES where %s != 'NULL'; """%(i)
        output.extend(execute_query(query)[0])
    return(html_table(header,output))

def modelStat(model):
    output = [model]
    #reactions
    reactionsQuery = """
    select count(*)
    from MODELS join MOD_REACT using (MID)
    where NAME LIKE "%s";
    """%(model)
    #metabolites
    metabolitesQuery = """
    select count(*)
    from MODELS join MOD_REACT using (MID)
    join REACTIONS using (RID)
    join STOICH on REACTIONS.RID = STOICH.REACTIONSID
    join METABOLITES using (METABOLITESID)
    where MODELS.NAME LIKE "%s";
    """%(model)
    extmetabolitesQuery = """
    select count(*)
    from MODELS join MOD_REACT using (MID)
    join REACTIONS using (RID)
    join STOICH on REACTIONS.RID = STOICH.REACTIONSID
    join METABOLITES using (METABOLITESID)
    where MODELS.NAME LIKE "%s" and COMPARTMENT = "c";
    """%(model)
    intmetabolitesQuery = """
    select count(*)
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

#query = submit_MODEL(model,media)
#print(execute_query(query))

printHead()
printHomepage()