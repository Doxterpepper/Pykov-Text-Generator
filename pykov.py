from flask import Flask, render_template, url_for, request, Response, redirect, session, escape
import sqlite3
import hashlib
import Markov
import pickle
import json

import db_init

app = Flask(__name__)
name = ''
pwd = ''

@app.route('/')
def index():
	t = get_default_text()	
	user_text = []
	if 'username' in session and session['username'] != None:
		user_text = get_user_text()
	return render_template("index.html", texts=(t, user_text))

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

# { 'title': 'some title',
#   'corpus': 'some corpus',
#   'token': 'user token' }
@app.route('/api/upload', methods=['POST'])
def upload():
	data = request.get_json(force=True)
	title = data['title']
	corpus = data['corpus']
	token = data['token']
	user_id = validate_token(token)
	if user_id < 0:
		return "401 Unauthorized"
	relations = Markov.gen_relation(corpus)
	conn = sqlite3.connect('pykov.db')
	cur = conn.cursor()
	print(corpus)
	cur.execute("""
		INSERT INTO Text
		(content, relations, uid, title)
		Values (?, ?, ?, ?);
	""", (corpus, pickle.dumps(relations), user_id, title))
	conn.commit()
	conn.close()
	return "success"

@app.route('/api/corpus', methods=['GET', 'POST'])
def get_corpus():
	print(request.is_json)
	data = request.get_json(force=True)
	if data == None:
		return "401"
	if not 'id' in data or data['id'] == None:
		return 'no id specified'
	user_id = 1
	if 'token' in data and data['token'] != None:
		if not 'id' in data:
			return "fail"
		user_id= validate_token(data['token'])
		if user_id < 0:
			return "401 unauthorized"
	conn = sqlite3.connect("pykov.db")
	c = conn.cursor()
	text = c.execute("""
		SELECT Title, Content
		FROM Text
		WHERE id=?
		AND uid=?
	""", (data['id'], user_id))
	ret = text.fetchall()
	return json.dumps({"title": ret[0][0], "text": ret[0][1]})
	

@app.route('/api/list', methods=['GET'])
def list():
	data = request.get_json()
	token = data['token']
	user_id = validate_token(token)
	if user_id < 0:
		return "401 Unauthorized"
	conn = sqlite3.connect('pykov.db')
	print(user_id)
	cur = conn.cursor()
	cur.execute("""
		SELECT id, title
		FROM Text
		WHERE uid=?
	""", (user_id,))
	rows = cur.fetchall()
	ret = []
	for row in rows:
		ret.append({'title': row[1], 'id': row[0]})
	return str(ret)
	
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
		print(user_id)
		texts = c.execute("""
			SELECT id, title
			FROM Text
			WHERE uid=?;
		""", (user_id,))
		for item in texts:
			t.append(item)
	return t
	
def validate_token(token):
	conn = sqlite3.connect('pykov.db')
	cur = conn.cursor()
	ret = cur.execute('select id from Users where token=?', (token,))
	rows = cur.fetchall()
	if len(rows) == 0:
		return -1
	return rows[0][0]
			
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

def genSaved(data):
	if not 'token' in data:
		return '401 Unauthorized'
	if not 'n' in data:
		n = 10
	else:
		n = data['n']

	user_id = validate_token(data['token'])
	if user_id < 0:
		return '401 Unauthorized'
	print(user_id)
	conn = sqlite3.connect('pykov.db')
	cur = conn.cursor()
	cur.execute('''
		SELECT relations
		FROM Text
		WHERE uid=?
		AND id=?
	''', (user_id, data['text-id']))
	ret = cur.fetchall()
	rel = ret[0]
	rel = pickle.loads(rel[0])
	return Markov.gen_with_relations(rel[0], n)

def genNewText(data):
	if 'n' in data:
		n = data['n']
	else:
		n = 10
	return Markov.gen_with_text(data['corpus'], n)
	
@app.route("/logout", methods=['POST'])
def logout():
	session['username'] = None
	session['token'] = None
	t = get_default_text()	
	return render_template("index.html", texts=(t, []))

app.secret_key = "b'\x07\x8c7>s\xe6\x88\xa2\xdf?[\xedy\xdf\xf0sL\xa4\xe63!-E7"


# Use the makrov algorithm to generate text
# based on the json data sent in a get or post.
# curl -XGET\
#      -H "Content-Type: application/json"\
#      -d '{"text": 'This is some corpus", "n": 10}'\
#      'some.url/api/gen'
@app.route('/api/gen', methods=['POST', 'GET'])
def userless_gen():
	data = request.get_json(force=True)
	if data == None:
		return "401 unauthorized"
	if 'text-id' in data:
		print('here')
		return json.dumps({"corpus": genSaved(data)})
	elif 'corpus' in data:
		return json.dumps({"corpus": genNewText(data)})
	return json.dumps({"error": True}) 
	
if __name__ == '__main__':
	app.run(port=4999, debug=True)
