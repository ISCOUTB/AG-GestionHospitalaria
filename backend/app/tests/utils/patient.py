from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import crud_patient, crud_document

from app.schemas import ResponsablesInfo, PatientAll, UserCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_document, random_password


def create_random_responsable() -> ResponsablesInfo:
    num_document = random_document()
    return ResponsablesInfo(num_doc_responsable=num_document)


def create_random_patient(db: Session, k: int = 10) -> PatientAll:
    user = create_random_user("patient", db, k)
    responsable = create_random_responsable()

    out = crud_patient.add_responsable(user.num_document, responsable, db)
    while out != 0:
        responsable = create_random_responsable()
        out = crud_patient.add_responsable(user.num_document, responsable, db)

    crud_document.add_history(user.num_document)
    return crud_patient.get_patient(user.num_document, db)


def get_patient_token(client: TestClient, db: Session) -> dict[str, str]:
    new_user = create_random_patient(db)

    login_data = {
        "username": new_user.num_document,
        "password": new_user.password,
        "rol": new_user.rol,
    }

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
