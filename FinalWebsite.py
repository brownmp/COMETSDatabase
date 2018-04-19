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
<title>Database Project</title>
<body>
<h1>Create Growth Curve from COMETS</h1>
<form name="myForm" action="https://bioed.bu.edu/cgi-bin/students_18/GroupB/FinalWebsite.py" method="POST">
<h2>Beginner Search: Select Model and Media</h2>


<div>
    <label for="model">Model</label>
    <input id="model" size="30" value = "%s" type="text" />

    <label for="media">Media</label>
    <input id="media" size="30" value = "%s" type="text" />

   <input type="submit" value="Submit" >

</div>

<h2>Advanced Search</h2>




</form>


<hr />
</body></html>
</table></body></html>

"""%(model,media)) 



# connect to the database
connection = pymysql.connect(host="bioed.bu.edu",db="groupB",user=,passwd=)

# get cursor
cursor = connection.cursor()

# run query
#cursor.execute(q)

# fetch results 
#cursor.fetchall()

# close the connection
cursor.close()
connection.close()
	
# return the results



print("""</body></html>""")
