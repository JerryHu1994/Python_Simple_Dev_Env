import json

def test_adduser(client):
    res = client.post("http://127.0.0.1:5000/adduser", json = {'name': 'Jake', 'age': 27, 'email': 'hjr01211@gmail.com'})
    assert res.status_code == 200
    assert {"Result": "Success"} == json.loads(res.get_data())
    #res2 = client.get("http://127.0.0.1:5000/getuser/Jake")
    #expected = {'name': 'Jake', 'age' : 27, 'email': 'hjr01211@gmail.com'}
    #print(res2.get_data())
    #assert expected == json.loads(res2.get_data())
