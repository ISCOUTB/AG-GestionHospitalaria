from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.patient import create_random_patient

endpoint = f"{settings.API_V1_STR}/documents"


def test_get_all_documents(
    client: TestClient, non_superuser_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)

    response = client.get(
        f"{endpoint}/all/{patient.num_document}", headers=non_superuser_token
    )

    assert response.status_code == 200

    content = response.json()

    assert "num_document" in content
    assert "history" in content
    assert "orders" in content
    assert "results" in content


def test_get_all(
    client: TestClient, non_superuser_token: dict[str, str]
) -> None:
    response = client.get(
        f"{endpoint}/all", headers=non_superuser_token
    )

    assert response.status_code == 200

    content = response.json()

    assert isinstance(content, list)

    example = content[0]

    assert "num_document" in example
    assert "history" in example
    assert "orders" in example
    assert "results" in example


def test_get_histories(
    client: TestClient, non_superuser_token: dict[str, str]
) -> None:
    response = client.get(
        f"{endpoint}/histories", headers=non_superuser_token
    )

    assert response.status_code == 200

    content = response.json()

    assert isinstance(content, list)


def test_get_orders(
    client: TestClient, non_superuser_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)
    response = client.get(
        f"{endpoint}/orders/{patient.num_document}", headers=non_superuser_token
    )

    assert response.status_code == 200

    content = response.json()

    assert "num_document" in content
    assert "filenames" in content
    assert "kind" in content


def test_get_results(
    client: TestClient, non_superuser_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)
    response = client.get(
        f"{endpoint}/results/{patient.num_document}", headers=non_superuser_token
    )

    assert response.status_code == 200

    content = response.json()

    assert "num_document" in content
    assert "filenames" in content
    assert "kind" in content

