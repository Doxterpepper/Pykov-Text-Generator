
"""
This python script creates the database with all the necessary
talbes for normal execution. There is no stated data when finished
but the following tables will exist.

----------------------------------
|             Users              |
----------------------------------
| username: text not null unique |
| password: text not null        |
| token: text not null unique    |
| id: integer primary key        |
----------------------------------

------------------------------------
|               Text               |
------------------------------------
| content: text not null           |
| relations: blob                  |
| uid: integer                     |
| title: text not null             | 
| id: integer primary key not null |
| uid: foreign key                 |
------------------------------------
"""

import sqlite3
import hashlib
import os
import hashlib
import re
import pickle
from . import Markov
conn = sqlite3.connect('pykov.db')

default_texts = []
admin = 'MrPykov'
password = "Th3yllN3v3rGu3ss"

c = conn.cursor()



def init_corpus():
	path = os.path.join("Pykov", "static", "texts")
	print(path)
	#Eric, change this so it's specific to your directory. Be sure that you are going all the way down to \static\texts\\
	#path = r"C:\Users\Eric\Pykov-Text-Generator\static\texts\\"
	for f in os.listdir(path):
		text_file = open(os.path.join("Pykov", "static", "texts", f), 'r')
		text = text_file.read()
		default_texts.append((re.split("\.", f)[0], text, pickle.dumps(Markov.gen_relation(text)), 1))
	for text in default_texts:
		c.execute('''
			INSERT INTO Text
			(title, content, relations, uid)
			VALUES (?, ?, ?, ?)
		''', text)

def create_user():
	hp = hashlib.md5(password.encode()).hexdigest()
	token = hashlib.md5(admin.encode()).hexdigest()
	c.execute("""
		INSERT INTO Users
		(username, password, token)
		VALUES (?, ?, ?)
	""", (admin, hp, token))

	
#c.execute('''
		#DROP TABLE Users;
#''')
#c.execute('''DROP TABLE Text;''')
	
try:
	# Create Users table
	c.execute('''
		CREATE TABLE Users(
		username TEXT NOT NULL UNIQUE, 
		password TEXT NOT NULL,
		token TEXT NOT NULL,
		id INTEGER PRIMARY KEY)
	''')


	# Create Text table
	c.execute('''
		CREATE TABLE Text(
		content TEXT NOT NULL,
		relations BLOB,
		uid INTEGER,
		title TEXT NOT NULL,
		id INTEGER PRIMARY KEY NOT NULL,
		FOREIGN KEY(uid) REFERENCES Users(id));
	''')

	create_user()
	init_corpus()

except sqlite3.OperationalError:
	print("warining table already created")

conn.commit()

conn.close()			
			
