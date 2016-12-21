from flask import Flask, render_template, url_for, request, Response, redirect, session, escape
from . import Markov
from . import db_init

app = Flask(__name__)

app.secret_key = "b'\x07\x8c7>s\xe6\x88\xa2\xdf?[\xedy\xdf\xf0sL\xa4\xe63!-E7"

import Pykov.views
import Pykov.api

if __name__ == '__main__':
	app.run(port=4999, debug=True)
