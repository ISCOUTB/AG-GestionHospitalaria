from sqlalchemy.orm import Session

from app.tests.utils.user import create_random_user
from app.tests.utils.patient import create_random_responsable, create_random_patient
from app.tests.utils.user import non_existent_document

from app import schemas
from app.crud import crud_patient


def test_get_patient(db: Session) -> None:
    patient_in = crud_patient.get_patient(non_existent_document, db)
    assert patient_in is None

    patient = create_random_patient(db)
    patient_in = crud_patient.get_patient(patient.num_document, db)
    assert patient_in.num_document == patient.num_document
    assert patient_in.num_doc_responsable == patient.num_doc_responsable


def test_add_responsable(db: Session) -> None:
    user = create_random_user("patient", db, 10)
    patient_eg = create_random_user("patient", db, 10)
    responsable = schemas.ResponsablesInfo()

    out = crud_patient.add_responsable(non_existent_document, responsable, db)
    assert out == 1

    responsable = schemas.ResponsablesInfo(num_doc_responsable=user.num_document)
    out = crud_patient.add_responsable(user.num_document, responsable, db)
    assert out == 2

    out = crud_patient.add_responsable(patient_eg.num_document, responsable, db)
    assert out == 3

    responsable = create_random_responsable()
    out = crud_patient.add_responsable(user.num_document, responsable, db)
    assert out == 0

    out = crud_patient.add_responsable(user.num_document, responsable, db)
    assert out == 4


def test_update_patient(db: Session) -> None:
    updated_info = schemas.ResponsablesInfo()
    out = crud_patient.update_patient(non_existent_document, updated_info, db)
    assert out == 1

    patient1 = create_random_patient(db)
    patient2 = create_random_patient(db)
    patient = create_random_user("patient", db, 10)

    responsable = schemas.ResponsablesInfo(num_doc_responsable=patient1.num_document)
    out = crud_patient.update_patient(patient1.num_document, responsable, db)
    assert out == 2

    responsable = schemas.ResponsablesInfo(num_doc_responsable=patient2.num_document)
    out = crud_patient.update_patient(patient2.num_document, responsable, db)
    assert out == 3

    responsable = schemas.ResponsablesInfo()
    out = crud_patient.update_patient(patient.num_document, responsable, db)
    assert out == 4

    responsable = create_random_responsable()
    out = crud_patient.add_responsable(patient1.num_document, responsable, db)
    if responsable.num_doc_responsable not in (
        patient1.num_document,
        patient2.num_document,
    ):
        assert out == 0


def test_delete_responsable(db: Session) -> None:
    patient = create_random_patient(db)

    out = crud_patient.delete_responsable(non_existent_document, db)
    assert out == 1

    out = crud_patient.delete_responsable(patient.num_document, db)
    assert out == 0

    out = crud_patient.delete_responsable(patient.num_document, db)
    assert out == 2
