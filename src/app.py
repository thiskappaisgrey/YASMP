#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

def run():
    app.run(host="0.0.0.0")

if __name__ == "__main__":
    run()
