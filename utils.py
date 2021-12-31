import json
import sqlite3
import redis

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
	print("Finish initializing SQL DB...")

def init_cache():
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
	print("Finish initializing user cache...")

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