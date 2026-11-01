
def test_register_and_login(client):

    response = client.post(
        "/auth/register",
        json={
            "company_name": "Example Company",
            "email": "admin@example.com",
            "full_name": "Admin User",
            "password": "StrongPassword123!"
        }
    )

    assert response.status_code == 201

    login = client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "StrongPassword123!"
        }
    )

    assert login.status_code == 200

    assert "access_token" in login.json()
