import json
import pickle
import sqlite3
import Pykov.Markov

def validate_token(token):
	conn = sqlite3.connect('pykov.db')
	cur = conn.cursor()
	ret = cur.execute('select id from Users where token=?', (token,))
	rows = cur.fetchall()
	if len(rows) == 0:
		return -1
	return rows[0][0]
			
	
"""
This doesn't seem to do anything right now
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
"""

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

