#!/usr/bin/env python3

from flask import current_app as app
from markupsafe import escape


@app.route("/")
def hello():
    return "Hello, World!"

# TODO Create CRUD for this
@app.route("/users/<username>")
def users(username):
    return "User %s" % escape(username)
# TODO Create CRUD for this
@app.route("/events/<eventname>")
def event(eventname):
    return "Event %s" % escape(eventname)

if __name__ == "__main__":
    app.run(host="localhost")
