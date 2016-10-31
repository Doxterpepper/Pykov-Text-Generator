from flask import Flask, render_template, url_for, request
import db_init
import Markov

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

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
	app.run('', 4999)
