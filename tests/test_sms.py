
def get_token(client):

    client.post(
        "/auth/register",
        json={
            "company_name": "SMS Company",
            "email": "sms@example.com",
            "full_name": "SMS Admin",
            "password": "StrongPassword123!"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "sms@example.com",
            "password": "StrongPassword123!"
        }
    )

    return response.json()["access_token"]


def test_sms_requires_consent(client):

    token = get_token(client)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    contact = client.post(
        "/contacts",
        headers=headers,
        json={
            "phone": "+919876543210",
            "name": "Test User",
            "sms_consent": False
        }
    ).json()

    response = client.post(
        "/sms/send",
        headers=headers,
        json={
            "contact_id": contact["id"],
            "message": "Test notification"
        }
    )

    assert response.status_code == 403


def test_sms_mock_send(client):

    token = get_token(client)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    contact = client.post(
        "/contacts",
        headers=headers,
        json={
            "phone": "+919876543211",
            "name": "Consented User",
            "sms_consent": True
        }
    ).json()

    response = client.post(
        "/sms/send",
        headers=headers,
        json={
            "contact_id": contact["id"],
            "message": "Test notification"
        }
    )

    assert response.status_code == 200

    assert response.json()["status"] == "simulated"
