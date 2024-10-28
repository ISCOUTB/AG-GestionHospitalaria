from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.bed import non_existent_bed
from app.tests.utils.bed import random_bed
from app.tests.utils.bed import create_random_bed
from app.tests.utils.hospitalizations import create_random_hospitalization

endpoint = f"{settings.API_V1_STR}/beds"


def test_add_bed(client: TestClient, admin_token: dict[str, str]) -> None:
    bed = random_bed()
    response = client.post(f"{endpoint}/", headers=admin_token, json=bed.model_dump())

    content = response.json()

    assert content["status"] == 201
    assert content["detail"] == "Cama agregada perfectamente"


def test_add_bed_room_already_with_bed(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    bed = create_random_bed(db)
    response = client.post(f"{endpoint}/", headers=admin_token, json=bed.model_dump())

    assert response.status_code == 409


def test_delete_bed(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    bed = create_random_bed(db)
    response = client.delete(f"{endpoint}/{bed.room}", headers=admin_token)

    content = response.json()

    assert content["status"] == 200
    assert content["detail"] == "Cama eliminada de la habitación"


def test_delete_bed_bed_not_found(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    response = client.delete(f"{endpoint}/{non_existent_bed}", headers=admin_token)

    assert response.status_code == 404


def test_delete_bed_bed_already_used(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    hospitalization = create_random_hospitalization(db)
    response = client.delete(f"{endpoint}/{hospitalization.room}", headers=admin_token)

    assert response.status_code == 409
