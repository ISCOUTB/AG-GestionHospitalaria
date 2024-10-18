from sqlalchemy.orm import Session

from app.crud import crud_patient

from app.schemas import ResponsablesInfo, PatientAll
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_document


def create_random_responsable() -> ResponsablesInfo:
    num_document = random_document()
    return ResponsablesInfo(num_doc_responsable=num_document)


def create_random_patient(db: Session, k: int = 10) -> PatientAll:
    user = create_random_user('patient', db, k)
    responsable = create_random_responsable()

    out = crud_patient.add_responsable(user.num_document, responsable, db)
    while out != 0:
        responsable = create_random_responsable()
        out = crud_patient.add_responsable(user.num_document, responsable, db)
    
    return crud_patient.get_patient(user.num_document, db)
