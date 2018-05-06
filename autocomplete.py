import sys
import pymysql
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
userInput = form.getvalue('model')


# generate query
query = 'SELECT NAME FROM MODELS WHERE NAME LIKE "' + userInput +'%";'

# connect to the database
connection = pymysql.connect(host="bioed.bu.edu",db="groupB",user="",passwd="")

# get cursor
cursor = connection.cursor()

# run query
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