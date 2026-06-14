def get_auth_header(client, username="alice", password="pass123"):
    client.post("/auth/register", json={"username": username, "password": password})
    response = client.post("/auth/login", data={"username": username, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_item_requires_auth(client):
    response = client.post("/items", json={"name": "Phone", "price": 499.99, "in_stock": True})
    assert response.status_code == 401


def test_create_item_success(client):
    headers = get_auth_header(client)
    response = client.post("/items", json={"name": "Phone", "price": 499.99, "in_stock": True}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Phone"
    assert data["owner_id"] == 1


def test_get_all_items(client):
    headers = get_auth_header(client)
    client.post("/items", json={"name": "Phone", "price": 499.99, "in_stock": True}, headers=headers)
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404


def test_update_item_by_owner(client):
    headers = get_auth_header(client, "alice", "pass123")
    create_resp = client.post("/items", json={"name": "Phone", "price": 499.99, "in_stock": True}, headers=headers)
    item_id = create_resp.json()["id"]

    response = client.put(f"/items/{item_id}", json={"name": "Updated Phone", "price": 450.0, "in_stock": False}, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Phone"


def test_update_item_by_non_owner_forbidden(client):
    alice_headers = get_auth_header(client, "alice", "pass123")
    create_resp = client.post("/items", json={"name": "Phone", "price": 499.99, "in_stock": True}, headers=alice_headers)
    item_id = create_resp.json()["id"]

    bob_headers = get_auth_header(client, "bob", "pass456")
    response = client.put(f"/items/{item_id}", json={"name": "Hacked", "price": 1.0, "in_stock": True}, headers=bob_headers)
    assert response.status_code == 403


def test_delete_item_by_owner(client):
    headers = get_auth_header(client, "alice", "pass123")
    create_resp = client.post("/items", json={"name": "Phone", "price": 499.99, "in_stock": True}, headers=headers)
    item_id = create_resp.json()["id"]

    response = client.delete(f"/items/{item_id}", headers=headers)
    assert response.status_code == 200

    get_resp = client.get(f"/items/{item_id}")
    assert get_resp.status_code == 404