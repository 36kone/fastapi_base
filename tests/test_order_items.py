import logging
import pytest


@pytest.fixture
def product(client, token):
    body = {
        "code": "002",
        "name": "order_item_product",
        "unit": "unit",
        "price": 5.0,
        "description": "test product for order item",
        "quantity": 10,
    }
    response = client.post(
        "/api/products", json=body, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    logging.info(f"CREATE PRODUCT FOR ORDER ITEMS: {data}")
    return data


@pytest.fixture
def order(client, token, product):
    body = {
        "description": "order for items",
        "order_items": [
            {
                "product_id": product["id"],
                "quantity": 2,
            }
        ],
    }
    response = client.post(
        "/api/orders", json=body, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    logging.info(f"CREATE ORDER FOR ORDER ITEMS: {data}")
    return data


@pytest.fixture
def order_item(client, token, order, product):
    body = {
        "order_id": order["id"],
        "product_id": product["id"],
        "quantity": 1,
    }
    response = client.post(
        "/api/order-items", json=body, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    logging.info(f"CREATE ORDER ITEM: {data}")
    return data


def test_create_order_item(client, token, order, product):
    body = {
        "order_id": order["id"],
        "product_id": product["id"],
        "quantity": 3,
    }
    response = client.post(
        "/api/order-items", json=body, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    logging.info(f"CREATE ORDER ITEM: {data}")
    assert data["order_id"] == order["id"]
    assert data["product_id"] == product["id"]


def test_get_order_items(client, token):
    response = client.get("/api/order-items", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    logging.info(f"GET ORDER ITEMS: {data}")
    assert isinstance(data, list)


def test_get_order_item_by_id(client, token, order_item):
    response = client.get(
        f"/api/order-items/{order_item['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    logging.info(f"GET ORDER ITEM BY ID: {data}")
    assert data["id"] == order_item["id"]


def test_update_order_item(client, token, order_item):
    body = {
        "id": order_item["id"],
        "quantity": 5,
    }
    response = client.put(
        f"/api/order-items/{order_item['id']}",
        json=body,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    logging.info(f"UPDATE ORDER ITEM: {data}")
    assert data["quantity"] == 5


def test_delete_order_item(client, token, order_item):
    response = client.delete(
        f"/api/order-items/{order_item['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    logging.info(f"DELETE ORDER ITEM: {data}")
