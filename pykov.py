
from flask import Flask, render_template, url_for, request, Response, redirect, session, escape
from flask_wtf import Form
from flask_login import login_required
import sqlite3
import hashlib

import db_init

app = Flask(__name__)
name = ''
pwd = ''
DATABASE = 'pykov.sqlite'
conn = sqlite3.connect(DATABASE)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/signup.html', methods=['POST', 'GET'])	
def signup():
	error = None
	if request.method == 'POST':
		username = request.form['userName']
		password = request.form['userPassword']
		passwordV = request.form['userPasswordVerification']
		validated = validateName(username)
		if password == passwordV:
			if validated:
				#SQL INSERT
				createUser(username,password)
				error = 'Account successfully created. Please log in.'
				return render_template("login.html", error=error)
			else: 
				#Username already exists in DB
				error = 'That username is already taken. Please try again.'
				return render_template("signup.html",error = error)
		else:
			error = 'Please make sure you type your password correctly.'
			return render_template("signup.html",error=error)
		return redirect(url_for(('index')))
	else:
		return render_template("signup.html")
	
@app.route('/login.html', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		#login and validate
		username = request.form['userName']
		password = request.form['userPassword']
		validated = validate(username, password)
		if validated == False:
			error = 'Incorrect username or password. Please try again.'
		else: #login successful
			session['username'] = username
			return redirect(url_for('index'))
		
		return render_template("login.html", error=error)
	else:
		return render_template("login.html")
		
	
	
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
			
			
			
def md5hash(hashed_pass, user_pass):
	return hashed_pass == hashlib.md5(user_pass.encode()).hexdigest()
			
			
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
	
def createUser(username, password):
	hashed_pass = hashlib.md5(password.encode()).hexdigest()
	conn = sqlite3.connect('pykov.db')
	with conn:
				cur = conn.cursor()
				cur.execute('''
				INSERT into USERS
				(username, password)
				VALUES (?,?);
				''',(username,hashed_pass,))
	conn.commit()
	conn.close()
	return True
	
	
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("index.html")
	
app.secret_key = "b'\x07\x8c7>s\xe6\x88\xa2\xdf?[\xedy\xdf\xf0sL\xa4\xe63!-E7"


# Use the makrov algorithm to generate text
# based on the json data sent in a get or post.
# curl -XGET\
#      -H "Content-Type: application/json"\
#      -d '{"text": 'This is some corpus", "n": 10}'\
#      'some.url/api/gen'
@app.route('/api/gen')
def userless_gen():
	data = request.get_json()
	return Markov.gen(data['text'], data['n'])

	
if __name__ == '__main__':
	app.run('', 4999, debug=True)
