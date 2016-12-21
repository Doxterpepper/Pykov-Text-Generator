from flask import Flask, render_template, url_for, request, Response, redirect, session, escape
from Pykov import app
from Pykov import view_helpers as vh
import sqlite3
import hashlib
import pickle
import json

@app.route('/')
def index():
	t = vh.get_default_text()
	user_text = []
	if 'username' in session and session['username'] != None:
		user_text = vh.get_user_text()
	return render_template("index.html", texts=(t, user_text))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	error = None
	if request.method == 'POST':
		username = request.form['userName']
		password = request.form['userPassword']
		passwordV = request.form['userPasswordVerification']
		validated = vh.validateName(username)
		if password == passwordV:
			if validated:
				#SQL INSERT
				vh.createUser(username,password)
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
	
@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		#login and validate
		username = request.form['userName']
		password = request.form['userPassword']
		validated = vh.validate(username, password)
		if validated == False:
			error = 'Incorrect username or password. Please try again.'
		else: #login successful
			session['username'] = username
			conn = sqlite3.connect('pykov.db')
			c = conn.cursor()
			token = c.execute("""
				SELECT token
				FROM Users
				WHERE username=?
			""", (username, ))
			token = token.fetchall()[0][0]
			session['token'] = token
			return redirect(url_for('index'))
		
		return render_template("login.html", error=error)
	else:
		return render_template("login.html")

@app.route("/logout", methods=['POST'])
def logout():
	session['username'] = None
	session['token'] = None
	t = vh.get_default_text()	
	return render_template("index.html", texts=(t, []))
