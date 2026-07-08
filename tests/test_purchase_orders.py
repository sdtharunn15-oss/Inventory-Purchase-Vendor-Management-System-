import uuid
from .conftest import client


def create_admin():

    unique = uuid.uuid4().hex[:8]

    client.post(
        "/auth/register",
        json={
            "username": f"admin_{unique}",
            "email": f"{unique}@example.com",
            "password": "password123",
            "role": "Admin"
        }
    )

    login = client.post(
        "/auth/login",
        data={
            "username": f"{unique}@example.com",
            "password": "password123"
        }
    )

    return login.json()["access_token"]


def test_create_purchase_order():

    token = create_admin()

    vendor = client.post(
        "/vendors/",
        json={
            "vendor_name": "HP",
            "email": f"{uuid.uuid4().hex[:8]}@example.com",
            "phone": "9999999999",
            "address": "Chennai"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    vendor_id = vendor.json()["id"]

    response = client.post(
        "/purchase-orders/",
        json={
            "vendor_id": vendor_id,
            "product_name": "Laptop",
            "quantity": 10,
            "unit_price": 50000,
            "expected_delivery_date": "2026-07-20"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_name"] == "Laptop"
    assert data["total_amount"] == 500000