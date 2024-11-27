from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

endpoint = settings.API_V1_STR


def test_get_stats(
    client: TestClient, non_superuser_token: dict[str, str]
) -> None:
    response = client.get(
        f"{endpoint}/stats", headers=non_superuser_token
    )

    assert response.status_code == 200

    content = response.json()

    assert "percent_occupation" in content
    assert "avg_stay" in content
    assert "admissions" in content
    assert "discharges" in content


def test_get_api_historial(
    client: TestClient, non_superuser_token: dict[str, str]
) -> None:
    response = client.get(
        f"{endpoint}/api-historial", headers=non_superuser_token
    )

    assert response.status_code == 200

    content = response.json()

    assert isinstance(content, list)

    if len(content) == 0:
        return None

    example = content[0]

    assert "username" in example
    assert "rol" in example
    assert "timestamp" in example
    assert "method" in example
    assert "url" in example
    assert "headers" in example
    assert "body" in example
    assert "process_time_ms" in example
    assert "status_code" in example
