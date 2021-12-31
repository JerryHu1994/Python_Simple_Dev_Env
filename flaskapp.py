from flask import Flask, request, jsonify
import json
import sqlite3
import redis

app = Flask(__name__)

@app.route("/adduser", methods=['POST'])
def add_user():
	content = request.get_json()
	user_name = content["name"]
	age = int(content["age"])
	email = content["email"]
	try:
		conn = sqlite3.connect('user.db')
		cursor = conn.cursor()
		cmd = "INSERT INTO users VALUES ('{0}', {1}, '{2}')".format(user_name, age, email)
		cursor.execute(cmd)
		conn.commit()
		conn.close()
	except Exception as exp:
		print('Exception during adduser: ', exp )
		return json.dumps({"Result": "Failed"}, 500, {'ContentType':'application/json'})

	return json.dumps({"Result": "Success"}), 200, {'ContentType':'application/json'}

@app.route("/getuser/<username>", methods=['GET'])
def get_user(username):
	r = redis.Redis(host='localhost', port=6379, db=0)
	if r.get(username):
		user_info = r.get(username)
	else:
		user_info = readuser_and_update_cache(username)
	if user_info is None:
		return json.dumps({"Error": "{} not found in system".format(username)}), 404, {'ContentType':'application/json'}
	else:
		return user_info, 200, {'ContentType':'application/json'}

@app.route("/addbalance/<username>", methods=['POST'])
def add_balance(username):
	content = request.get_json()
	to_add = int(content["balance"])
	r = redis.Redis(host='localhost', port=6379, db=0)
	if not r.get(username):
		user_info = readuser_and_update_cache(username)
		if user_info == None:
			return json.dumps({"Result": "Failed", "Error": "{} not found in system".format(username)}), 404, {
				'ContentType': 'application/json'}

	user_info = json.loads(r.get(username))
	new_balance = int(user_info["balance"]) + to_add
	user_info["balance"] = new_balance
	r.set(username, json.dumps(user_info))
	return json.dumps({"Result": "Success", "Balance": new_balance}), 200, {'ContentType':'application/json'}

@app.route("/getbalance/<username>", methods=['GET'])
def get_balance(username):
	r = redis.Redis(host='localhost', port=6379, db=0)

	if r.get(username) == 0:
		return json.dumps({"Error": "No balance was found for user {} in system".format(username)}), 404, {'ContentType':'application/json'}
	else:
		response = r.get(username)
		return json.dumps({"name": username, "Balance": int(json.loads(response)["balance"])}), 200, {'ContentType':'application/json'}

def init_SQLDB():
	try:
		conn = sqlite3.connect('user.db')
		c = conn.cursor()
		c.execute("""CREATE TABLE IF NOT EXISTS users(
			name text,
			age integer,
			email text
			)""")
		conn.commit()
		conn.close()
	except Exception as exp:
		print('Exp: ', exp)
		raise exp
	print("Finish initializing SQL DB")

def init_Cache():
	try:
		conn = sqlite3.connect('user.db')
		c = conn.cursor()
		cmd = "SELECT * FROM users"
		c.execute(cmd)
		users = c.fetchall()
		conn.commit()
		conn.close()
	except Exception as exp:
		print('User cache initialization failed. Exp: ', exp)
	r = redis.Redis(host='localhost', port=6379, db=0)
	for user in users:
		r.set(user[0], json.dumps({"age": user[1], "email": user[2], "balance": 0, "activities": []}))
	print("Finish initializing user cache")

def readuser_and_update_cache(username):
	try:
		conn = sqlite3.connect('user.db')
		c = conn.cursor()
		cmd = "SELECT * FROM users WHERE name='{}'".format(name)

		c.execute(cmd)
		user = c.fetchone()

		conn.commit()
		conn.close()
	except Exception as exp:
		print('Exception during getuser: ', exp)
		return None
	# update cache
	user_info = {"age": user[1], "email": user[2], "balance": 0}
	r.set(user[0], json.dumps(user_info))
	return username

if __name__ == '__main__':
	init_SQLDB()
	init_Cache()
	app.run(debug=True)