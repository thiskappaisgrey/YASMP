#!/usr/bin/env python3

from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

# TODO Create CRUD for this
@app.route("/users/<username>")
def users():
    return "User %s" % escape(username)
# TODO Create CRUD for this
@app.route("/events/<eventname>")
def events()
    return "Event %s" % escape(eventname)

if __name__ == "__main__":
    app.run(host="localhost")
