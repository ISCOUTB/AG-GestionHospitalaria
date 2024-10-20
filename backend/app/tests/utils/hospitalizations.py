import random

from app import schemas

from sqlalchemy.orm import Session

from app.tests.utils.bed import create_random_bed
from app.tests.utils.doctor import create_doctor_info
from app.tests.utils.patient import create_random_patient

from app.crud import crud_hospitalization


def create_random_hospitalization(db: Session) -> schemas.RegisterHospitalization:
    patient = create_random_patient(db)
    doctor = create_doctor_info(db)
    bed = create_random_bed(db)

    hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        room=bed.room
    )

    out = crud_hospitalization.add_hospitalization(hospitalization, db)
    while out != 0:
        hospitalization = create_random_hospitalization(db)
        out = crud_hospitalization.add_hospitalization(hospitalization, db)

    return hospitalization
