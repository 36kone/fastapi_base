import logging

import pytest


@pytest.fixture
def product(client, token):
    body = {
        "code": "001",
        "name": "product",
        "unit": "unit",
        "price": 0.0,
        "description": "test",
        "quantity": 1,
    }
    response = client.post(
        "/api/products", json=body, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    logging.info(f"CREATE PRODUCT FOR ORDERS: {data}")
    return data


@pytest.fixture
def order(client, token, product):
    body = {
        "description": "test",
        "order_items": [
            {
                "product_id": product["id"],
                "quantity": 1,
            }
        ],
    }
    response = client.post(
        "/api/orders", json=body, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    logging.info(f"CREATE ORDERS: {data}")
    return data


def test_create_order(client, token, product):
    body = {
        "description": "test",
        "order_items": [
            {
                "product_id": product["id"],
                "quantity": 1,
            }
        ],
    }
    response = client.post(
        "/api/orders", json=body, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    logging.info(f"CREATE ORDERS: {data}")
    assert data


def test_get_orders(client, token):
    response = client.get("/api/orders", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    logging.info(f"GET ORDERS: {data}")
    assert isinstance(data, list)


def test_get_order_by_id(client, token, order):
    response = client.get(
        f"/api/orders/{order["id"]}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order["id"]


def test_update_order(client, token, order):
    body = {
        "id": str(order["id"]),
        "description": "test update",
    }
    response = client.put(
        f"/api/orders/{order["id"]}",
        json=body,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    logging.info(f"UPDATE ORDER: {data}")
    assert data["id"] == order["id"]


def test_delete_order(client, token, order):
    response = client.delete(
        f"/api/orders/{order["id"]}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    logging.info(f"DELETE ORDER: {data}")
