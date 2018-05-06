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
			<h1>Biological Databases Project</h1>
			<p>Virtual experiments using COMETS!</p> 
		</div>
		<div class="container-fluid" style="padding-left: 50px; padding-right: 50px;">
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
	</body>
	</html>
	""")

printHead()
printAdvancedSearch()