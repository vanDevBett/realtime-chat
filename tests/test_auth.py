def test_register(client):
    response = client.post("/auth/register", json={
        "email": "new@test.com",
        "full_name": "New User",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "new@test.com"


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "email": "dup@test.com",
        "full_name": "User",
        "password": "password123"
    })
    response = client.post("/auth/register", json={
        "email": "dup@test.com",
        "full_name": "User",
        "password": "password123"
    })
    assert response.status_code == 400


def test_login(client):
    client.post("/auth/register", json={
        "email": "login@test.com",
        "full_name": "Login User",
        "password": "password123"
    })
    response = client.post("/auth/login", data={
        "username": "login@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "email": "wrong@test.com",
        "full_name": "Wrong User",
        "password": "password123"
    })
    response = client.post("/auth/login", data={
        "username": "wrong@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/auth/login", data={
        "username": "nouser@test.com",
        "password": "password123"
    })
    assert response.status_code == 401