from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.bed import non_existent_bed
from app.tests.utils.bed import random_bed
from app.tests.utils.bed import create_random_bed
from app.tests.utils.hospitalizations import create_random_hospitalization

endpoint = f"{settings.API_V1_STR}/beds"


def test_add_bed(client: TestClient, superuser_token: dict[str, str]) -> None:
    bed = random_bed()
    response = client.post(f"{endpoint}/", headers=superuser_token, json=bed.model_dump())

    assert response.status_code == 201

    content = response.json()
    assert content["detail"] == "Cama agregada perfectamente"


def test_add_bed_room_already_with_bed(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    bed = create_random_bed(db)
    response = client.post(f"{endpoint}/", headers=superuser_token, json=bed.model_dump())

    assert response.status_code == 409


def test_delete_bed(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    bed = create_random_bed(db)
    response = client.delete(f"{endpoint}/{bed.room}", headers=superuser_token)

    content = response.json()

    assert content["status"] == 200
    assert content["detail"] == "Cama eliminada de la habitación"


def test_delete_bed_bed_not_found(
    client: TestClient, superuser_token: dict[str, str]
) -> None:
    response = client.delete(f"{endpoint}/{non_existent_bed}", headers=superuser_token)

    assert response.status_code == 404


def test_delete_bed_bed_already_used(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    hospitalization = create_random_hospitalization(db)
    response = client.delete(f"{endpoint}/{hospitalization.room}", headers=superuser_token)

    assert response.status_code == 409
