from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.user import non_existent_document, random_document, random_password
from app.tests.utils.doctor import create_doctor_info
from app.tests.utils.patient import create_random_patient

from app.crud import crud_admin
from app import schemas

endpoint = f"{settings.API_V1_STR}/consultations"


def test_get_consultation(client: TestClient, superuser_token: dict[str, str]) -> None:
    response = client.get(
        f"{endpoint}/", headers=superuser_token
    )

    assert response.status_code == 200

    content = response.json()
    assert isinstance(content, list)

    if len(content) == 0:
        return None

    consultation_example = content[0]

    assert "num_doc_patient" in consultation_example
    assert "num_doc_doctor" in consultation_example
    assert "area" in consultation_example
    assert "day" in consultation_example


def test_add_consultation(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)
    doctor = create_doctor_info(db)

    new_consultation = schemas.Consultation(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        area="area1",
    )
    json = new_consultation.model_dump()
    json["day"] = new_consultation.day.strftime("%Y-%m-%d")

    response = client.post(f"{endpoint}/", headers=doctor_token, json=json)

    assert response.status_code == 201

    content = response.json()
    assert content["detail"] == "Consulta médica agregada"


def test_add_consultation_patient_not_found(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    doctor = create_doctor_info(db)

    new_consultation = schemas.Consultation(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=non_existent_document,
        area="area1",
    )
    json = new_consultation.model_dump()
    json["day"] = new_consultation.day.strftime("%Y-%m-%d")

    response = client.post(f"{endpoint}/", headers=doctor_token, json=json)

    assert response.status_code == 404


def test_add_consultation_doctor_not_found(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)

    new_consultation = schemas.Consultation(
        num_doc_doctor=non_existent_document,
        num_doc_patient=patient.num_document,
        area="area1",
    )
    json = new_consultation.model_dump()
    json["day"] = new_consultation.day.strftime("%Y-%m-%d")

    response = client.post(f"{endpoint}/", headers=doctor_token, json=json)

    assert response.status_code == 404


def test_add_consultation_patient_doctor_same_document(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    document = random_document()
    new_user = schemas.UserCreate(
        num_document=document,
        rol="patient",
        password=random_password(10),
    )
    crud_admin.create_user(new_user, db)

    new_user.rol = "doctor"
    crud_admin.create_user(new_user, db)

    new_consultation = schemas.Consultation(
        num_doc_doctor=document,
        num_doc_patient=document,
        area="area1",
    )
    json = new_consultation.model_dump()
    json["day"] = new_consultation.day.strftime("%Y-%m-%d")

    response = client.post(f"{endpoint}/", headers=doctor_token, json=json)

    assert response.status_code == 409
