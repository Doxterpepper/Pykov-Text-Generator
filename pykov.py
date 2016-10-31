from flask import Flask, render_template, url_for, request
import db_init
import Markov

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/api/gen')
def userless_gen():
	data = request.get_json()
	return Markov.gen(data['text'], data['n'])

if __name__ == '__main__':
	app.run('', 4999)
