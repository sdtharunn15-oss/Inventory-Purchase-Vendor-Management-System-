import uuid

from .conftest import client

def get_admin_token():

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


def test_create_vendor():

    token = get_admin_token()

    response = client.post(
        "/vendors/",
        json={
            "vendor_name": "Dell",
            "email": "dell@example.com",
            "phone": "9876543210",
            "address": "Chennai"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert response.json()["vendor_name"] == "Dell"