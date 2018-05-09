#!/usr/bin/env python
# print content-type
print("Content-Type:text/html\n")
print("""
	<html>
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/smoothness/jquery-ui.css">
		<script src="//code.jquery.com/jquery-1.12.4.js"></script>
		<script src="//code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css">
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script>
	</head>
	<body>
		<div class="jumbotron text-center">
			<h1>Biological Databases Project</h1>
			<p>Virtual experiments using COMETS!</p>
		</div>

		<div class="container">
			<div class="col-md-6">
			</div>
			<div class="col-md-6">
				<h2>All Metabolites:</h2>
				<ul id="allMets" class="list-group">""")

with open("metsList.txt") as f:
	for line in f:
		print('<li class="list-group-item">' + line + '</li>')

print("""
				</ul>
			</div>
			<div class="col-md-6">
			</div>
		</div>
	</body>
</html>
	""")