import json

def test_add_and_get_user(client):
    add_response = client.post("http://127.0.0.1:5000/adduser", json = {'name': 'Jerry', 'age': 27, 'email': 'hjr01211@gmail.com'})
    assert add_response.status_code == 200
    assert {"Result": "Success"} == json.loads(add_response.get_data())

    get_response = client.get("http://127.0.0.1:5000/getuser/Jerry")
    assert get_response.status_code == 200
    assert {"age": 27, "email": "hjr01211@gmail.com", "balance": 0, "activities": []} == json.loads(get_response.get_data())

def test_get_user_not_found(client):
    get_response = client.get("http://127.0.0.1:5000/getuser/notfounduser")
    assert get_response.status_code == 404
    assert {"Error": "notfounduser not found in system"} == json.loads(get_response.get_data())