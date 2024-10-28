from fastapi.testclient import TestClient

from app.core.config import settings
from app import schemas

endpoint = f'{settings.API_V1_STR}/login'


def test_login_access_token(client: TestClient) -> None:
    login_data = schemas.UserLogin(
        num_document=settings.FIRST_SUPERUSER,
        rol='admin',
        password=settings.FIRST_SUPERUSER_PASSWORD
    )

    response = client.post(
        f'{endpoint}/access-token',
        data=login_data.model_dump()
    )

    token = response.json()
    assert "access_token" in token
    assert token["access_token"]


def test_login_access_token_user_incorrect(client: TestClient) -> None:
    login_data = schemas.UserLogin(
        num_document=settings.FIRST_SUPERUSER,
        rol='admin',
        password=settings.FIRST_SUPERUSER_PASSWORD
    )

    response = client.post(
        f'{endpoint}/access-token',
        data=login_data.model_dump()
    )

    assert response.status_code == 401
