import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.user import non_existent_document, random_document, random_password
from app.tests.utils.bed import non_existent_bed
from app.tests.utils.bed import create_random_bed
from app.tests.utils.doctor import create_doctor_info
from app.tests.utils.patient import create_random_patient
from app.tests.utils.hospitalizations import create_random_hospitalization

from app import schemas
from app.crud import crud_admin

endpoint = f"{settings.API_V1_STR}/hospitalizations"


def test_get_hospitalization(client: TestClient, superuser_token: dict[str, str]) -> None:
    response = client.get(
        f"{endpoint}/", headers=superuser_token
    )

    assert response.status_code == 200

    content = response.json()
    assert isinstance(content, list)

    if len(content) == 0:
        return None

    hospitalization_example = content[0]

    assert "num_doc_patient" in hospitalization_example
    assert "num_doc_doctor" in hospitalization_example
    assert "entry_day" in hospitalization_example
    assert "last_day" in hospitalization_example


def test_add_hospitalization(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)
    doctor = create_doctor_info(db)
    bed = create_random_bed(db)

    hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        room=bed.room,
    )
    json = hospitalization.model_dump()
    json["entry_day"] = hospitalization.entry_day.strftime("%Y-%m-%d")

    response = client.post(f"{endpoint}/", headers=doctor_token, json=json)

    assert response.status_code == 201

    content = response.json()
    assert content["detail"] == "Hospitalización agregada"


def test_add_hospitalization_patient_not_found(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    doctor = create_doctor_info(db)
    bed = create_random_bed(db)

    hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=non_existent_document,
        room=bed.room,
    )
    json = hospitalization.model_dump()
    json["entry_day"] = hospitalization.entry_day.strftime("%Y-%m-%d")

    response = client.post(f"{endpoint}/", headers=doctor_token, json=json)

    assert response.status_code == 404


def test_add_hospitalization_doctor_not_found(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)
    bed = create_random_bed(db)

    hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=non_existent_document,
        num_doc_patient=patient.num_document,
        room=bed.room,
    )
    json = hospitalization.model_dump()
    json["entry_day"] = hospitalization.entry_day.strftime("%Y-%m-%d")

    response = client.post(f"{endpoint}/", headers=doctor_token, json=json)

    assert response.status_code == 404


def test_add_hospitalization_bed_not_found(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    patient = create_random_patient(db)
    doctor = create_doctor_info(db)

    hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        room=non_existent_bed,
    )
    json = hospitalization.model_dump()
    json["entry_day"] = hospitalization.entry_day.strftime("%Y-%m-%d")

    response = client.post(f"{endpoint}/", headers=doctor_token, json=json)

    assert response.status_code == 404


def test_add_hospitalization_patient_doctor_same_document(
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
    bed = create_random_bed(db)

    hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=document,
        num_doc_patient=document,
        room=bed.room,
    )
    json = hospitalization.model_dump()
    json["entry_day"] = hospitalization.entry_day.strftime("%Y-%m-%d")

    response = client.post(f"{endpoint}/", headers=doctor_token, json=json)

    assert response.status_code == 409


def test_add_hospitalization_bed_already_used(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    hospitalization = create_random_hospitalization(db)
    patient = create_random_patient(db)
    doctor = create_doctor_info(db)

    new_hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        room=hospitalization.room,
    )
    json = hospitalization.model_dump()
    json["entry_day"] = hospitalization.entry_day.strftime("%Y-%m-%d")

    response = client.post(f"{endpoint}/", headers=doctor_token, json=json)

    assert response.status_code == 409


def test_add_hospitalization_patient_already_hospitalized(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    hospitalization = create_random_hospitalization(db)
    json = hospitalization.model_dump()
    json["entry_day"] = hospitalization.entry_day.strftime("%Y-%m-%d")

    response = client.post(f"{endpoint}/", headers=doctor_token, json=json)

    assert response.status_code == 409


def test_discharge_hospitalization(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    hospitalization = create_random_hospitalization(db)
    discharge = schemas.DischargeHospitalization()
    json = discharge.model_dump()
    json["last_day"] = discharge.last_day.strftime("%Y-%m-%d")

    response = client.put(
        f"{endpoint}/{hospitalization.num_doc_patient}",
        headers=doctor_token,
        json=json,
    )

    assert response.status_code == 200

    content = response.json()
    assert content["detail"] == "Paciente dado de alta del sistema"


def test_discharge_hospitalization_patient_not_found(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    discharge = schemas.DischargeHospitalization()
    json = discharge.model_dump()
    json["last_day"] = discharge.last_day.strftime("%Y-%m-%d")

    response = client.put(
        f"{endpoint}/{non_existent_document}",
        headers=doctor_token,
        json=json,
    )

    assert response.status_code == 404


def test_discharge_hospitalization_bad_date_formatting_date_older(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    hospitalization = create_random_hospitalization(db)
    discharge = schemas.DischargeHospitalization(
        last_day=datetime.date.today() + datetime.timedelta(days=10)
    )
    json = discharge.model_dump()
    json["last_day"] = discharge.last_day.strftime("%Y-%m-%d")

    response = client.put(
        f"{endpoint}/{hospitalization.num_doc_patient}",
        headers=doctor_token,
        json=json,
    )

    assert response.status_code == 400


def test_discharge_hospitalization_bad_date_formatting_date_less(
    client: TestClient, doctor_token: dict[str, str], db: Session
) -> None:
    hospitalization = create_random_hospitalization(db)
    discharge = schemas.DischargeHospitalization(
        last_day=hospitalization.entry_day - datetime.timedelta(days=10)
    )
    json = discharge.model_dump()
    json["last_day"] = discharge.last_day.strftime("%Y-%m-%d")

    response = client.put(
        f"{endpoint}/{hospitalization.num_doc_patient}",
        headers=doctor_token,
        json=json,
    )

    assert response.status_code == 400
