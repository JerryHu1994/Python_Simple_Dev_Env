import json

def test_add_and_balance_user(client):
    adduser_response = client.post("http://127.0.0.1:5000/adduser", json = {'name': 'JerryBalanceTest', 'age': 27, 'email': 'hjr01211@gmail.com'})
    assert adduser_response.status_code == 200
    assert {"Result": "Success"} == json.loads(adduser_response.get_data())

    addbalance_res = client.post("http://127.0.0.1:5000/addbalance/JerryBalanceTest", json = {'balance': 200})
    assert addbalance_res.status_code == 200
    assert {"Result": "Success", "Balance": 200} == json.loads(addbalance_res.get_data())

    addbalance_res2 = client.post("http://127.0.0.1:5000/addbalance/JerryBalanceTest", json={'balance': 300})
    assert addbalance_res2.status_code == 200
    assert {"Result": "Success", "Balance": 500} == json.loads(addbalance_res2.get_data())

    getbalance_res = client.get("http://127.0.0.1:5000/getbalance/JerryBalanceTest")
    assert getbalance_res.status_code == 200
    assert {"name": "JerryBalanceTest", "Balance": 500} == json.loads(getbalance_res.get_data())

def test_add_balance_user_not_found(client):
    addbalance_res = client.post("http://127.0.0.1:5000/addbalance/notfounduser", json = {'balance': 200})
    assert addbalance_res.status_code == 404
    assert {"Result": "Failed", "Error": "notfounduser not found in system."} == json.loads(addbalance_res.get_data())

def test_get_balance_user_not_found(client):
    getbalance_res = client.get("http://127.0.0.1:5000/getbalance/notfounduser")
    assert getbalance_res.status_code == 404
    assert {"Error": "No balance was found for user notfounduser in system."} == json.loads(getbalance_res.get_data())
