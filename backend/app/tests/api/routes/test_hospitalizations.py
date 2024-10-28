import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.user import non_existent_document
from app.tests.utils.bed import non_existent_bed
from app.tests.utils.bed import create_random_bed
from app.tests.utils.doctor import create_doctor_info
from app.tests.utils.patient import create_random_patient
from app.tests.utils.hospitalizations import create_random_hospitalization

from app import schemas

endpoint = f'{settings.API_V1_STR}/hospitalizations'


def test_add_hospitalization(client: TestClient, doctor_token: dict[str, str], db: Session) -> None:
    patient = create_random_patient(db)
    doctor = create_doctor_info(db)
    bed = create_random_bed(db)

    hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        room=bed.room
    )

    response = client.post(
        f'{endpoint}/',
        headers=doctor_token,
        json=hospitalization.model_dump()
    )

    content = response.json()
    assert content['status'] == 201
    assert content['detail'] == 'Hospitalización agregada'


def test_add_hospitalization_patient_not_found(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    doctor = create_doctor_info(db)
    bed = create_random_bed(db)

    hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=non_existent_document,
        room=bed.room
    )

    response = client.post(
        f'{endpoint}/',
        headers=doctor_token,
        json=hospitalization.model_dump()
    )

    assert response.status_code == 404


def test_add_hospitalization_doctor_not_found(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)
    bed = create_random_bed(db)

    hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=non_existent_document,
        num_doc_patient=patient.num_document,
        room=bed.room
    )

    response = client.post(
        f'{endpoint}/',
        headers=doctor_token,
        json=hospitalization.model_dump()
    )

    assert response.status_code == 404


def test_add_hospitalization_bed_not_found(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)
    doctor = create_doctor_info(db)

    hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        room=non_existent_bed
    )

    response = client.post(
        f'{endpoint}/',
        headers=doctor_token,
        json=hospitalization.model_dump()
    )

    assert response.status_code == 404


def test_add_hospitalization_bed_already_used(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    hospitalization = create_random_hospitalization(db)
    patient = create_random_patient(db)
    doctor = create_doctor_info(db)

    new_hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        room=hospitalization.room
    )

    response = client.post(
        f'{endpoint}/',
        headers=doctor_token,
        json=new_hospitalization.model_dump()
    )

    assert response.status_code == 409


def test_add_hospitalization_patient_already_hospitalized(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    hospitalization = create_random_hospitalization(db)

    response = client.post(
        f'{endpoint}/',
        headers=doctor_token,
        json=hospitalization.model_dump()
    )

    assert response.status_code == 409


def test_discharge_hospitalization(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    hospitalization = create_random_hospitalization(db)
    discharge = schemas.DischargeHospitalization()
    
    response = client.put(
        f'{endpoint}/{hospitalization.num_doc_patient}',
        headers=doctor_token,
        json=discharge.model_dump()
    )

    content = response.json()

    assert content['status'] == 200
    assert content['detail'] == 'Paciente dado de alta del sistema'


def test_discharge_hospitalization_patient_not_found(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    discharge = schemas.DischargeHospitalization()

    response = client.put(
        f'{endpoint}/{non_existent_document}',
        headers=doctor_token,
        json=discharge.model_dump()
    )

    assert response.status_code == 404


def test_discharge_hospitalization_bad_date_formatting(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    hospitalization = create_random_hospitalization(db)
    discharge = schemas.DischargeHospitalization(
        last_day=datetime.date.today() + datetime.timedelta(days=10) 
    )

    response = client.put(
        f'{endpoint}/{hospitalization.num_doc_patient}',
        headers=doctor_token,
        json=discharge.model_dump()
    )

    assert response.status_code == 400
