#!/usr/bin/python3
import pymysql
import sys
import cgi
import cgitb
cgitb.enable()

# print content-type
print("Content-Type:text/html\n")

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

def printAdvancedSearch():
	print("""
	<body>
		<div class="jumbotron text-center">
			<h1>Database Project</h1>
			<p>Virtual experiments using COMETS!</p> 
		</div>
		<div class="row" style="padding-left: 50px;">
			<div class="col-sm-4">
				<form name="myForm" action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/Advanced.py" method="POST">
					<h2>Advanced Search!</h2>

					<div class="form-group">

					    <label for="model">Model</label>

					    <input id="model" class="form-control" type="text" name="model" placeholder="Choose Models">

					    <br>

					    <label for="reactions">Reactions</label>

					    <input id="reactions" class="form-control" type="text" name="reactions" placeholder="Choose Models">

					    <br>

					    <label for="metabolites">Metabolites</label>

					    <input id="metabolites" class="form-control" type="text" name="metabolites" placeholder="Choose Models">

					    <br>

					    <label for="media">Media</label>

					    <select class="form-control">
					    	<option value=""</option>
							<option value="Basal">Basal</option>
							<option value="M9">M9</option>
						</select>

					</div>

					<input type="submit" class="btn" value="Submit" >
				</form>
				<form action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/Homepage.py">
    				<input type="submit" class="btn" value="Basic" />
				</form>
			</div>
		</div>
	</body>
	</html>
	""")

printHead()
printAdvancedSearch()