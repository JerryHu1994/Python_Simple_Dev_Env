from flask import Flask, request, jsonify
import json
import sqlite3
import redis

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/adduser", methods=['POST'])
def add_user():
	content = request.get_json()
	return json.dumps(content), 200, {'ContentType':'application/json'} 



if __name__ == '__main__':
	app.run(debug=True)