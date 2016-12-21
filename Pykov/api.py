from flask import Flask, render_template, url_for, request, Response, redirect, session, escape
from Pykov import app
import Pykov.api_helpers as ah
import sqlite3
import json
import pickle
from Pykov import Markov

# { 'title': 'some title',
#   'corpus': 'some corpus',
#   'token': 'user token' }
@app.route('/api/upload', methods=['POST'])
def upload():
	data = request.get_json(force=True)
	title = data['title']
	corpus = data['corpus']
	token = data['token']
	user_id = ah.validate_token(token)
	if user_id < 0:
		return "401 Unauthorized"
	relations = Markov.gen_relation(corpus)
	conn = sqlite3.connect('pykov.db')
	cur = conn.cursor()
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
	data = request.get_json(force=True)
	if data == None:
		return "401"
	if not 'id' in data or data['id'] == None:
		return 'no id specified'
	user_id = 1
	if 'token' in data and data['token'] != None:
		if not 'id' in data:
			return "fail"
		user_id= ah.validate_token(data['token'])
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
	user_id = ah.validate_token(token)
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
		return json.dumps({"corpus": ah.genSaved(data)})
	elif 'corpus' in data:
		return json.dumps({"corpus": ah.genNewText(data)})
	return json.dumps({"error": True}) 

