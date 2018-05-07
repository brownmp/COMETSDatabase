import sys
import pymysql
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
userInput = form.getvalue('model')


# generate query
query = 'SELECT NAME FROM MODELS WHERE NAME LIKE "' + userInput +'%";'

# login to the database and run query
with open('login.txt') as f:
	lines=f.readlines()
	username=lines[0].strip()
	password=lines[1].strip()

connection = pymysql.connect(host="bioed.bu.edu",db="groupB",user=username,passwd=password)
cursor = connection.cursor()
cursor.execute(query)

# fetch results 
results = cursor.fetchall()

names = []

for val in results:
    names += val

# close the connection
cursor.close()
connection.close()

print("Content-Type:text/html\n")
print(names)