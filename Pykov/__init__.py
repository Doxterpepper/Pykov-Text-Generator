from flask import Flask, render_template, url_for, request, Response, redirect, session, escape
from . import Markov
from . import db_init
app = Flask(__name__)

app.secret_key = "b'\x07\x8c7>s\xe6\x88\xa2\xdf?[\xedy\xdf\xf0sL\xa4\xe63!-E7"

import Pykov.views


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
	cur.execute("""
		INSERT INTO Text
		(content, relations, uid, title)
		#Values (?, ?, ?, ?);
	#""", (corpus, pickle.dumps(relations), user_id, title))
	conn.commit()
	conn.close()
	return "success"

@app.route('/api/corpus', methods=['GET', 'POST'])
def get_corpus():
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

def validate_token(token):
	conn = sqlite3.connect('pykov.db')
	cur = conn.cursor()
	ret = cur.execute('select id from Users where token=?', (token,))
	rows = cur.fetchall()
	if len(rows) == 0:
		return -1
	return rows[0][0]
			

			
def validateTitle(title, token):
	conn = sqlite3.connect('pykov.db')
	valid = true
	with conn:
				cur = con.cursor()
				cur.execute('''SELECT title FROM Text
				WHERE token=?''',(token,))
				rows = cur.fetchall()
				for row in rows:
					dbTitle = row[0]
					if dbTitle == title:
						valid = False
	return valid
	
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
		return json.dumps({"corpus": genSaved(data)})
	elif 'corpus' in data:
		return json.dumps({"corpus": genNewText(data)})
	return json.dumps({"error": True}) 
	
if __name__ == '__main__':
	app.run(port=4999, debug=True)
