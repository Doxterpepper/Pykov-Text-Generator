from flask import Flask, render_template, url_for
import db_init

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")
@app.route('/login.html')
def login():
	return render_template("login.html")
@app.route('/signup.html')
def signup():
	return render_template("signup.html")

if __name__ == '__main__':
	app.run('', 4999)
