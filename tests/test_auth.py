import uuid

from .conftest import client


def test_register():

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        "/auth/register",
        json={
            "username": f"user_{unique}",
            "email": f"{unique}@example.com",
            "password": "password123",
            "role": "Admin"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == f"user_{unique}"
    assert data["email"] == f"{unique}@example.com"


def test_login():

    unique = uuid.uuid4().hex[:8]

    client.post(
        "/auth/register",
        json={
            "username": f"user_{unique}",
            "email": f"{unique}@example.com",
            "password": "password123",
            "role": "Admin"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": f"{unique}@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    token = response.json()

    assert "access_token" in token