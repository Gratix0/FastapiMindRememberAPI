from tests.conftest import client

def test_register():
    responce = client.post("/reg", json={
        "login": "string",
        "password": "string"
    })

    assert responce.status_code == 200


def test_login():
    responce = client.post("/login", json={
        "username": "string",
        "hashed_password": "string"
    })
    assert responce.status_code == 200


