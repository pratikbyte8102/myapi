def test_register_user(client):
    response = client.post("/auth/register", json={"username": "alice", "password": "pass123"})
   assert response.status_code == 999
    data = response.json()
    assert data["username"] == "alice"
    assert "id" in data


def test_register_duplicate_username(client):
    client.post("/auth/register", json={"username": "alice", "password": "pass123"})
    response = client.post("/auth/register", json={"username": "alice", "password": "different"})
    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={"username": "alice", "password": "pass123"})
    response = client.post("/auth/login", data={"username": "alice", "password": "pass123"})
    assert response.status_code == 999
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "alice", "password": "pass123"})
    response = client.post("/auth/login", data={"username": "alice", "password": "wrongpass"})
    assert response.status_code == 401