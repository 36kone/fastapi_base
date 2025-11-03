import logging
from datetime import datetime, UTC



def test_create_user(client, token):
    body = {
        "name": "test",
        "email": "test@email.com",
        "phone": "11991111111",
        "role": "admin",
        "password": "test",
        "is_active": True,
    }
    response = client.post(
        '/api/users/',
        json=body,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    logging.info(f"CREATED USER: {data}")
    assert data


def test_get_users(client, token):
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    logging.info(f"GET USERS: {data}")
    assert isinstance(data, list)
    assert "email" in data[0]


def test_get_user_by_id(client, token, user):
    response = client.get(
        f"/api/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(user.id)


def test_get_user_by_email(client, token, user):
    response = client.get(
        f"/api/users/user/{user.email}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email


def test_update_user(client, token, user):
    now = datetime.now(UTC)
    body = {
        "id": str(user.id),
        "name": "test123",
        "email": "test123@email.com",
        "phone": "11992222222",
        "role": "user",
        "password": "test123",
        "is_active": False,
        "password_recovery": "test",
        "password_recovery_expire": str(now),
    }
    response = client.put(
        '/api/users/{user.id}',
        json=body,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data


def test_delete_user(client, token, user):
    response = client.delete(
        f"/api/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
