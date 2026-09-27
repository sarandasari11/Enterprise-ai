from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.main import create_app


app = create_app()
client = TestClient(app)


def test_register_login_and_me_flow() -> None:
    email = f"phase4-{uuid4()}@example.com"
    payload = {
        "email": email,
        "name": "Phase Four User",
        "password": "StrongPass123!",
    }

    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == 200
    assert register_response.json()["email"] == payload["email"]
    assert "password_hash" not in register_response.json()

    login_response = client.post(
        "/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    assert token

    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == payload["email"]

    logout_response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "Logged out successfully"


def test_invalid_token_is_rejected() -> None:
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer not-a-valid-token"},
    )
    assert response.status_code == 401
