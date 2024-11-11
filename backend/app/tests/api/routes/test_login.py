from fastapi.testclient import TestClient

from app.core.config import settings
from app import schemas

endpoint = f"{settings.API_V1_STR}/login"


def test_login_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
        "rol": "admin",
    }

    response = client.post(f"{endpoint}/access-token", data=login_data)

    token = response.json()
    assert "access_token" in token
    assert token["access_token"]


def test_login_access_token_user_incorrect(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
        "rol": "doctor",
    }

    response = client.post(f"{endpoint}/access-token", data=login_data)

    assert response.status_code == 401
