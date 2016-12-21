import sqlite3
import hashlib
from flask import Flask, render_template, url_for, request, Response, redirect, session, escape

def createUser(username, password):
	hashed_pass = hashlib.md5(password.encode()).hexdigest()
	token = hashlib.md5(username.encode()).hexdigest()
	conn = sqlite3.connect('pykov.db')
	with conn:
		cur = conn.cursor()
		cur.execute('''
		INSERT into USERS
		(username, password, token)
		VALUES (?, ?, ?);
		''',(username, hashed_pass, token))
	conn.commit()
	conn.close()
	return True

def validateName(username):
	conn = sqlite3.connect('pykov.db')
	valid = True
	with conn:
		cur = conn.cursor()
		cur.execute('''SELECT username FROM Users''')
		rows = cur.fetchall()
		for row in rows:
			dbName = row[0]
			if dbName == username:
				valid = False
	return valid

def md5hash(hashed_pass, user_pass):
	return hashed_pass == hashlib.md5(user_pass.encode()).hexdigest()

def validate(username, password):
	conn = sqlite3.connect('pykov.db')
	valid = False
	with conn:
				cur = conn.cursor()
				cur.execute('''SELECT * FROM Users''')
				rows = cur.fetchall()
				for row in rows:
					dbName = row[0]
					dbPass = row[1]
					if dbName==username:
						valid=md5hash(dbPass,password)
	return valid

def get_default_text():
	t = []
	conn = sqlite3.connect("pykov.db")
	c = conn.cursor()
	texts = c.execute("""
		SELECT id, title
		FROM Text
		WHERE uid=1;
	""")
	for item in texts:
		t.append(item)
	c.close()
	return t

def get_user_text():
	conn = sqlite3.connect("pykov.db")
	c = conn.cursor()
	t = []
	if 'username' in session and session['username'] != None:
		user_id = c.execute("""
			SELECT id
			FROM Users
			WHERE username=?
		""", (session['username'],))
		user_id = user_id.fetchall()[0][0]
		texts = c.execute("""
			SELECT id, title
			FROM Text
			WHERE uid=?;
		""", (user_id,))
		for item in texts:
			t.append(item)
	return t
