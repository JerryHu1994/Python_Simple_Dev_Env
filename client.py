import requests as req 

resp = req.post("http://127.0.0.1:5000/adduser", json={
    'name':'Jake',
    'age': 27,
    'email': 'hjr01211@gmail.com'})
print (resp)

resp = req.get("http://127.0.0.1:5000/getuser/Jake")
print (resp.json())