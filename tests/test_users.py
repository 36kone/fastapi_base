def test_get_users(client, token):
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "email" in data[0]


def test_get_user_by_id(client, token, user):
    response = client.get(
        f"/api/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email


def test_get_user_by_email(client, token, user):
    response = client.get(
        f"/api/users/user/{user.email}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email