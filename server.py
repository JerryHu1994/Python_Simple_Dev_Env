from flask import Flask, request, jsonify
import json
import sqlite3
import redis
import utils

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
		print('Exception during adduser: ', exp)
		return json.dumps({"Result": "Failed"}, 500, {'ContentType': 'application/json'})

	return json.dumps({"Result": "Success"}), 200, {'ContentType': 'application/json'}

@app.route("/getuser/<username>", methods=['GET'])
def get_user(username):
	r = redis.Redis(host='localhost', port=6379, db=0)
	if r.get(username):
		user_info = r.get(username)
	else:
		user_info = utils.readuser_and_update_cache(username)
	if user_info is None:
		return json.dumps({"Error": "{} not found in system".format(username)}), 404, \
			   {'ContentType': 'application/json'}
	else:
		return user_info, 200, {'ContentType': 'application/json'}

@app.route("/addbalance/<username>", methods=['POST'])
def add_balance(username):
	content = request.get_json()
	to_add = int(content["balance"])
	r = redis.Redis(host='localhost', port=6379, db=0)
	if not r.get(username):
		user_info = utils.readuser_and_update_cache(username)
		if user_info == None:
			return json.dumps({"Result": "Failed", "Error": "{} not found in system".format(username)}), 404, \
				   {'ContentType': 'application/json'}

	user_info = json.loads(r.get(username))
	new_balance = int(user_info["balance"]) + to_add
	user_info["balance"] = new_balance
	r.set(username, json.dumps(user_info))
	return json.dumps({"Result": "Success", "Balance": new_balance}), 200, {'ContentType':'application/json'}

@app.route("/getbalance/<username>", methods=['GET'])
def get_balance(username):
	r = redis.Redis(host='localhost', port=6379, db=0)

	if r.get(username) == 0:
		return json.dumps({"Error": "No balance was found for user {} in system".format(username)}), 404, \
			   {'ContentType':'application/json'}
	else:
		response = r.get(username)
		return json.dumps({"name": username, "Balance": int(json.loads(response)["balance"])}), 200, \
			   {'ContentType':'application/json'}

if __name__ == '__main__':
	utils.init_SQLDB()
	utils.init_cache()
	app.run(debug=True)