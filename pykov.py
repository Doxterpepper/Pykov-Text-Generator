from flask import Flask, render_template, url_for, request, Response, redirect, session, escape
from flask_wtf import Form
from flask_login import LoginManager, UserMixin, login_required
import sqlite3
import hashlib

import db_init

app = Flask(__name__)
#login_manger = LoginManager()
#login_manager.init_app(app)
name = ''
pwd = ''
DATABASE = 'pykov.sqlite'
conn = sqlite3.connect(DATABASE)

@app.route('/')
def index():
	return render_template("index.html")

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
			
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("index.html")
	
app.secret_key = "b'\x07\x8c7>s\xe6\x88\xa2\xdf?[\xedy\xdf\xf0sL\xa4\xe63!-E7"

	
if __name__ == '__main__':
	app.run('', 4999, debug=True)
