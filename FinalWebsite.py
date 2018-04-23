#!/usr/bin/python3
import pymysql
import sys
import cgi
import cgitb
cgitb.enable()

# print content-type
print("Content-Type:text/html")


#get the form
form = cgi.FieldStorage()
model = form.getvalue("model")
media = form.getvalue("media")


print("""
<html>

<head>

<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" 
integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">

<script src="http://code.jquery.com/jquery-1.11.1.min.js"</script>
<script src="js/jquery.ui.autocomplete.html.js" />
<script src="http://code.jquery.com/ui/1.10.4/jquery-ui.min.js"</script>

<div class="jumbotron text-center">
  <h1>Database Project</h1>
  <p>Virtual experiments using COMETS!</p> 
</div>


</head>

<body>
<div class="row" style="padding-left: 50px;">
  <div class="col-sm-4">
  	<form name="myForm" action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/FinalWebsite.py" method="POST">
		<h2>Select Model and Media</h2>


		<script src="bootstrap-autocomplete.min.js"></script>

		<form autocomplete="off" action="/action_page.php">
		  <div class="autocomplete" style="width:300px;">
		    <input id="model" class="form-control" type="text" name="myCountry" placeholder="Choose Models">
		  </div>
		  <input type="submit" class="btn">
		</form>

		<div class="form-group">
		    <label for="model">Model</label>
		    <input id="model" class="form-control" size="30" value = "%s" type="text" />

		    <label for="media">Media</label>
		    <input id="media" class="form-control" size="30" value = "%s" type="text" />

		   	<input type="submit" class="btn" value="Submit" >

		</div>

		<button type="button" class="btn">Advanced Search</button>
	</form>
  </div>
</div>
</body></html>
</table></body></html>

"""%(model,media)) 

print("""</body></html>""")


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

#query = submit_MODEL(model,media)
#print(execute_query(query))




















