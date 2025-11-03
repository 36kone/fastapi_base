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
        '/api/products',
        json=body,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    logging.info(f"CREATE PRODUCT: {data}")
    return data


def test_create_product(client, token):
    body = {
        "code": "001",
        "name": "product",
        "unit": "unit",
        "price": 0.0,
        "description": "test",
        "quantity": 1,
    }
    response = client.post(
        '/api/products',
        json=body,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    logging.info(f"CREATE PRODUCT: {data}")
    assert data


def test_get_products(client, token):
    response = client.get(
        "/api/products",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    logging.info(f"GET PRODUCTS: {data}")
    assert isinstance(data, list)


def test_get_product_by_id(client, token, product):
    response = client.get(
        f"/api/products/{product['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product["id"]


def test_update_product(client, token, product):
    body = {
        "id": str(product["id"]),
        "code": "002",
        "name": "test123",
        "unit": "meters",
        "price": 1.0,
        "description": "test",
        "quantity": 2,
    }
    response = client.put(
        f"/api/products/{product['id']}",
        json=body,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product["id"]


def test_delete_product(client, token, product):
    response = client.delete(
        f"/api/products/{product['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
