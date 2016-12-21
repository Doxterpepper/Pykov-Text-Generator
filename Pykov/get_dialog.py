import re

f = open("static/texts/Pulp Fiction.txt", 'r')

for line in f:
	val = re.match("\s{25}(?!\s)(\w+ )*", line)
	if val != None:
		print(val.string)
