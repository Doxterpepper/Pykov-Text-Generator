import sqlite3
import hashlib
conn = sqlite3.connect('pykov.db')

c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS Users''')
c.execute('''DROP TABLE IF EXISTS Text''')
c.execute('''
CREATE TABLE Users(
username TEXT NOT NULL UNIQUE, 
password TEXT NOT NULL,
id INTEGER PRIMARY KEY)''')
user_pass = 'admin'
hashed_pass = hashlib.md5(user_pass.encode()).hexdigest()
c.execute('''
INSERT INTO Users
(username, password)
VALUES ('admin',?);''',(hashed_pass,))
c.execute('''
CREATE TABLE Text(
content TEXT NOT NULL,
relations BLOB,
uid INTEGER,
title TEXT NOT NULL,
id INTEGER PRIMARY KEY NOT NULL,
FOREIGN KEY(uid) REFERENCES Users(id)
);''')
			

conn.commit()

conn.close()			
			