import sqlite3
conn = sqlite3.connect('pykov.db')

c = conn.cursor()

try:
	c.execute('''CREATE TABLE Users
			(username text, password text, token text, userid integer)''')
			
	c.execute('''CREATE TABLE Text
			(content text, relations blob, token text, title text, id integer)''')
except sqlite3.OperationalError:
	print ("Warning: Database already created")
			

conn.commit()

conn.close()			
			