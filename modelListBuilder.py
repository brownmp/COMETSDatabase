import pymysql

# generate query
query = 'SELECT NAME FROM MODELS;'

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

# close the connection
cursor.close()
connection.close()

# write results to text file
file = open('modelList.txt','w') 
 
for val in results:
	currentModel = str(val)
	currentModel = currentModel[2:-3]

	file.write(currentModel)
	file.write('\n')

file.close() 