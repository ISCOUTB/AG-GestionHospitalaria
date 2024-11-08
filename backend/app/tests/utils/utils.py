import random
import string

from fastapi.testclient import TestClient

from app.core.config import settings


def random_document() -> str:
    list_numbers: list[int] = random.choices(range(0, 10), k=1_000_000)
    return "random_" + "".join(str(x) for x in list_numbers)


def random_password(k: int) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=k))


def get_superuser_token(client: TestClient) -> dict[str, str]:
    login = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
        "rol": "admin",
    }

    response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login)
    tokens = response.json()
    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
