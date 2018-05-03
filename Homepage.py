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
#model = form.getvalue("model")
#media = form.getvalue("media")

def printHead():
	print("""
	<html>
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>


		<script>
			$( "#model" ).autocomplete({
				minLength: 2,
				source: function(request, response) {
					$.ajax({
						type: "POST",
						url: "https://bioed.bu.edu/cgi-bin/students_18/GroupB/autocomplete.py",
						data: "tag_part=" + request.term,
						dataType: "html",
						success: function(data) {
							response(data);
						}
					});
				},
			});
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
			<ul class="nav nav-tabs">
				<li class="active"><a data-toggle="tab" href="#Basic">Basic</a></li>
				<li><a data-toggle="tab" href="#Advanced">Advanced</a></li>
				<li><a data-toggle="tab" href="#About">About</a></li>
				<li><a data-toggle="tab" href="#Help">Help</a></li>
			</ul>

			<div class="tab-content">
			    <div id="Basic" class="tab-pane fade in active">
				    <div class="container-fluid" style="padding-left: 50px;">
						<form name="myForm" action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/Homepage.py" method="POST">
							<div class="row">
								<div class="col">
									<div class="col-8">
										<h2>Select Model and Media</h2>

										<div class="form-group">

										    <label for="model">Model</label>

										    <input id="model" class="form-control" type="text" name="model" placeholder="Choose Models">

										    <br>

										    <label for="media">Media</label>

										    <select class="form-control">
										    	<option value="">Choose Media</option>
												<option value="Basal">Basal</option>
												<option value="M9">M9</option>
											</select>

											<br>

										</div>

										<input type="submit" class="btn btn-success" value="Submit" >
									</div>
									<div class="col-4">
									</div>
								</div>

								<div class="col">""")
	graph()
	print("""
		    </div>
		    <div id="Advanced" class="tab-pane fade">
			    <div class="row">
					<h1>Advanced Search</h1>
				</div>
				<form name="myForm" action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/Advanced.py" method="POST">
					<div class="row">
						<div class="col">
							<div class="form-group">
							    <label for="model">Model</label>
							    <input id="model" class="form-control" type="text" name="model" placeholder="Choose Models">
							    <br>
							    <label for="media">Media</label>
							    <select class="form-control">
							    	<option value=""</option>
									<option value="Basal">Basal</option>
									<option value="M9">M9</option>
								</select>
							</div>
							<input type="submit" class="btn btn-success" value="Submit" >
							<a href="https://bioed.bu.edu/cgi-bin/students_18/GroupB/Homepage.py" class="btn btn-secondary">Basic</a>
						</div>

						<div class="col">
							<div class="form-group">
								<label for="reactions">Reactions</label>
								<input id="reactions" class="form-control" type="text" name="reactions" placeholder="Choose Reactions">
								<br>
							</div>
						</div>

						<div class="col">
							<div class="form-group">
							<label for="metabolites">Metabolites</label>
							<input id="metabolites" class="form-control" type="text" name="metabolites" placeholder="Choose Metabolites">
							<br>
						</div>
					</div>	
				</form>
		    </div>
		</div>			
	""")


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
	# connect to the database
	connection = pymysql.connect(host="bioed.bu.edu",db="groupB",user="ahamel19",passwd="Sparticus6")

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
	print("""
		</div>
				</div>
			</form>
		</div>
	</body>
	</html>

		""")

#query = submit_MODEL(model,media)
#print(execute_query(query))

printHead()
printHomepage()