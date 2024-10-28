from sqlalchemy.orm import Session

from app.tests.utils.patient import create_random_patient
from app.tests.utils.doctor import create_doctor_info
from app.tests.utils.user import non_existent_document

from app import schemas
from app.crud import crud_consultation


def test_add_consultation(db: Session) -> None:
    patient = create_random_patient(db)
    doctor = create_doctor_info(db)

    new_consultation = schemas.Consultation(
        num_doc_doctor=non_existent_document,
        num_doc_patient=patient.num_document,
        area="area1",
    )

    out = crud_consultation.add_consultation(new_consultation, db)
    assert out == 2

    new_consultation = schemas.Consultation(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=non_existent_document,
        area="area1",
    )

    out = crud_consultation.add_consultation(new_consultation, db)
    assert out == 1

    new_consultation = schemas.Consultation(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        area="area1",
    )

    out = crud_consultation.add_consultation(new_consultation, db)
    assert out == 0
