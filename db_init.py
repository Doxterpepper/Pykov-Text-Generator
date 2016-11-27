
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
conn = sqlite3.connect('pykov.db')

c = conn.cursor()

#c.execute('''DROP TABLE IF EXISTS Users''')
#c.execute('''DROP TABLE IF EXISTS Text''')
try:
	c.execute('''
	CREATE TABLE Users(
	username TEXT NOT NULL UNIQUE, 
	password TEXT NOT NULL,
	token TEXT NOT NULL,
	id INTEGER PRIMARY KEY)''')

	"""
	user_pass = 'admin'
	hashed_pass = hashlib.md5(user_pass.encode()).hexdigest()
	c.execute('''
	INSERT INTO Users
	(username, password)
	VALUES ('admin',?);''',(hashed_pass,))
	"""
	c.execute('''

	CREATE TABLE Text(
	content TEXT NOT NULL,
	relations BLOB,
	uid INTEGER,
	title TEXT NOT NULL,
	id INTEGER PRIMARY KEY NOT NULL,
	FOREIGN KEY(uid) REFERENCES Users(id)
	);''')
except sqlite3.OperationalError:
	print("warining table already created")

conn.commit()

conn.close()			
			
