from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.user import create_random_user
from app.tests.utils.user import non_existent_document, random_document
from app.tests.utils.patient import create_random_patient, create_random_responsable

from app import schemas

from app.crud import crud_patient

endpoint = f"{settings.API_V1_STR}/patients"


def test_get_patient(
    client: TestClient, nonpatient_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)

    response = client.get(
        f"{endpoint}/{patient.num_document}", headers=nonpatient_token
    )

    assert response.status_code == 200

    content = response.json()

    assert patient.num_document == content["num_document"]
    assert patient.num_doc_responsable == content["num_doc_responsable"]


def test_get_patient_patient_not_found(
    client: TestClient, nonpatient_token: dict[str, str]
) -> None:
    response = client.get(
        f"{endpoint}/{non_existent_document}", headers=nonpatient_token
    )

    assert response.status_code == 404


def test_add_responsable(
        client: TestClient, nonpatient_token: dict[str, str], db: Session
) -> None:
    patient = create_random_user("patient", db, 10)

    new_responsable_info = create_random_responsable()

    response = client.post(
        f"{endpoint}/{patient.num_document}",
        headers=nonpatient_token,
        json=new_responsable_info.model_dump(),
    )

    assert response.status_code == 201

    content = response.json()
    assert content["detail"] == "Información del responsable agregada"


def test_add_responsable_patient_not_found(
    client: TestClient, nonpatient_token: dict[str, str]
) -> None:
    new_responsable_info = schemas.ResponsablesInfo(
        num_doc_responsable=random_document(),
    )

    response = client.post(
        f"{endpoint}/{non_existent_document}",
        headers=nonpatient_token,
        json=new_responsable_info.model_dump(),
    )

    assert response.status_code == 404


def test_add_responsable_patient_cannot_be_his_responsable(
    client: TestClient, nonpatient_token: dict[str, str], db: Session
) -> None:
    patient = create_random_user("patient", db, 10)
    new_responsable_info = schemas.ResponsablesInfo(
        num_doc_responsable=patient.num_document
    )

    response = client.post(
        f"{endpoint}/{patient.num_document}",
        headers=nonpatient_token,
        json=new_responsable_info.model_dump(),
    )

    assert response.status_code == 400


def test_add_responsable_patient_cannot_be_responsable(
    client: TestClient, nonpatient_token: dict[str, str], db: Session
) -> None:
    patient1 = create_random_user("patient", db, 10)
    patient2 = create_random_user("patient", db, 10)

    new_responsable_info = schemas.ResponsablesInfo(
        num_doc_responsable=patient2.num_document
    )

    response = client.post(
        f"{endpoint}/{patient1.num_document}",
        headers=nonpatient_token,
        json=new_responsable_info.model_dump(),
    )

    assert response.status_code == 409


def test_add_responsable_responsable_found(
    client: TestClient, nonpatient_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)

    new_responsable_info = create_random_responsable()

    response = client.post(
        f"{endpoint}/{patient.num_document}",
        headers=nonpatient_token,
        json=new_responsable_info.model_dump(),
    )

    assert response.status_code == 409


def test_update_patient(
    client: TestClient, nonpatient_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)

    new_document = f"{patient.num_doc_responsable}New"
    new_relationship = "Parents"
    new_responsable_info = schemas.ResponsablesInfo(
        num_doc_responsable=new_document,
        relationship_responsable=new_relationship,
    )

    response = client.put(
        f"{endpoint}/{patient.num_document}",
        headers=nonpatient_token,
        json=new_responsable_info.model_dump(),
    )

    assert response.status_code == 200

    content = response.json()
    assert content["detail"] == "Información del responsable actualizada"

    patient_in = crud_patient.get_patient(patient.num_document, db)
    assert patient_in.num_doc_responsable == new_document
    assert patient_in.relationship_responsable == new_relationship


def test_update_patient_patient_not_found(
    client: TestClient, nonpatient_token: dict[str, str]
) -> None:
    new_relationship = "Parents"
    new_responsable_info = schemas.ResponsablesInfo(
        relationship_responsable=new_relationship
    )

    response = client.put(
        f"{endpoint}/{non_existent_document}",
        headers=nonpatient_token,
        json=new_responsable_info.model_dump(),
    )

    assert response.status_code == 404


def test_update_patient_patient_cannot_be_his_responsable(
    client: TestClient, nonpatient_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)
    new_responsable_info = schemas.ResponsablesInfo(
        num_doc_responsable=patient.num_document
    )

    response = client.put(
        f"{endpoint}/{patient.num_document}",
        headers=nonpatient_token,
        json=new_responsable_info.model_dump(),
    )

    assert response.status_code == 400


def test_update_patient_patient_cannot_be_responsable(
    client: TestClient, nonpatient_token: dict[str, str], db: Session
) -> None:
    patient1 = create_random_patient(db)
    patient2 = create_random_patient(db)

    new_responsable_info = schemas.ResponsablesInfo(
        num_doc_responsable=patient2.num_document
    )

    response = client.put(
        f"{endpoint}/{patient1.num_document}",
        headers=nonpatient_token,
        json=new_responsable_info.model_dump(),
    )

    assert response.status_code == 409


def test_update_patient_responsable_not_found(
    client: TestClient, nonpatient_token: dict[str, str], db: Session
) -> None:
    patient = create_random_user("patient", db, 10)
    empty_responsable = schemas.ResponsablesInfo()

    response = client.put(
        f"{endpoint}/{patient.num_document}",
        headers=nonpatient_token,
        json=empty_responsable.model_dump(),
    )

    assert response.status_code == 404


def test_delete_responsable(
    client: TestClient, nonpatient_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)

    response = client.delete(
        f"{endpoint}/{patient.num_document}", headers=nonpatient_token
    )

    assert response.status_code == 200

    content = response.json()
    assert content["detail"] == "Información del responsable eliminada"

    patient_in = crud_patient.get_patient(patient.num_document, db)
    assert patient.num_document == patient_in.num_document
    assert patient_in.num_doc_responsable is None


def test_delete_responsable_patient_not_found(
    client: TestClient, nonpatient_token: dict[str, str]
) -> None:
    response = client.delete(
        f"{endpoint}/{non_existent_document}", headers=nonpatient_token
    )

    assert response.status_code == 404


def test_delete_responsable_responsable_not_found(
    client: TestClient, nonpatient_token: dict[str, str], db: Session
) -> None:
    patient = create_random_user("patient", db, 10)
    response = client.delete(
        f"{endpoint}/{patient.num_document}", headers=nonpatient_token
    )

    assert response.status_code == 404
