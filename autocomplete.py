#!/usr/bin/python3
import sys
import pymysql
import json

data = sys.stdin.read()
myjson = json.loads(data)

userInput = myjson['input']

# generate query
query = 'SELECT NAME FROM MODELS WHERE NAME LIKE "' + userInput +'%";'

#query = 'SELECT NAME FROM MODELS WHERE NAME LIKE "Clo%";'

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

print('Content-Type: application/json\n\n')
print(json.dumps(names))