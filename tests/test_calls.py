
def test_call_requires_consent(client):

    client.post(
        "/auth/register",
        json={
            "company_name": "Voice Company",
            "email": "voice@example.com",
            "full_name": "Voice Admin",
            "password": "StrongPassword123!"
        }
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "voice@example.com",
            "password": "StrongPassword123!"
        }
    )

    headers = {
        "Authorization": f"Bearer {login.json()['access_token']}"
    }

    contact = client.post(
        "/contacts",
        headers=headers,
        json={
            "phone": "+919876543212",
            "name": "Test User",
            "voice_consent": False
        }
    ).json()

    response = client.post(
        "/calls/start",
        headers=headers,
        json={
            "contact_id": contact["id"]
        }
    )

    assert response.status_code == 403


def test_call_mock_with_consent(client):

    client.post(
        "/auth/register",
        json={
            "company_name": "Voice Company 2",
            "email": "voice2@example.com",
            "full_name": "Voice Admin",
            "password": "StrongPassword123!"
        }
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "voice2@example.com",
            "password": "StrongPassword123!"
        }
    )

    headers = {
        "Authorization": f"Bearer {login.json()['access_token']}"
    }

    contact = client.post(
        "/contacts",
        headers=headers,
        json={
            "phone": "+919876543213",
            "name": "Consented User",
            "voice_consent": True
        }
    ).json()

    response = client.post(
        "/calls/start",
        headers=headers,
        json={
            "contact_id": contact["id"]
        }
    )

    assert response.status_code == 200

    assert response.json()["status"] == "simulated"
