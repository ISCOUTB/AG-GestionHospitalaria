from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.user import non_existent_document
from app.tests.utils.doctor import create_doctor_info
from app.tests.utils.patient import create_random_patient

from app import schemas

endpoint = f'{settings.API_V1_STR}/consultations'


def test_add_consultation(client: TestClient, doctor_token: dict[str, str], db: Session) -> None:
    patient = create_random_patient(db)
    doctor = create_doctor_info(db)

    new_consultation = schemas.Consultation(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        area='area1'
    )

    response = client.post(
        f'{endpoint}/',
        headers=doctor_token,
        json=new_consultation.model_dump()
    )

    content = response.json()

    assert content['status'] == 201
    assert content['detail'] == 'Consulta médica agregada'


def test_add_consultation_patient_not_found(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    doctor = create_doctor_info(db)

    new_consultation = schemas.Consultation(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=non_existent_document,
        area='area1'
    )

    response = client.post(
        f'{endpoint}/',
        headers=doctor_token,
        json=new_consultation.model_dump()
    )

    assert response.status_code == 404


def test_add_consultation_doctor_not_found(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)

    new_consultation = schemas.Consultation(
        num_doc_doctor=non_existent_document,
        num_doc_patient=patient.num_document,
        area='area1'
    )

    response = client.post(
        f'{endpoint}/',
        headers=doctor_token,
        json=new_consultation.model_dump()
    )

    assert response.status_code == 404
