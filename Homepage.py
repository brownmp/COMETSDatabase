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
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
		<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
	</head>
	""")

def printHomepage():
	print("""
	<body>
		<div class="jumbotron text-center">
			<h1>Database Project</h1>
			<p>Virtual experiments using COMETS!</p> 
		</div>
		<div class="row" style="padding-left: 50px;">
			<div class="col-sm-4">
				<form name="myForm" action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/FinalWebsite.py" method="POST">
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

					</div>

					<input type="submit" class="btn btn-success" value="Submit" >
				</form>
				<form action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/Advanced.py">
					<input type="submit" class="btn btn-secondary" value="Advanced" />
				</form>
			</div>
		</div>
	</body>
	</html>
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

#query = submit_MODEL(model,media)
#print(execute_query(query))

printHead()
printHomepage()
graph()