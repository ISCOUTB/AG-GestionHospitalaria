import datetime
from sqlalchemy.orm import Session

from app.tests.utils.hospitalizations import create_random_hospitalization
from app.tests.utils.patient import create_random_patient
from app.tests.utils.doctor import create_doctor_info
from app.tests.utils.bed import create_random_bed, non_existent_bed
from app.tests.utils.user import non_existent_document, random_document, random_password

from app import schemas
from app.crud import crud_hospitalization, crud_admin


def test_add_hospitalization(db: Session) -> None:
    hospitalization = create_random_hospitalization(db)
    patient = create_random_patient(db)
    doctor = create_doctor_info(db)
    bed = create_random_bed(db)

    new_hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=non_existent_document,
        num_doc_patient=patient.num_document,
        room=bed.room,
    )

    out = crud_hospitalization.add_hospitalization(new_hospitalization, db)
    assert out == 2

    new_hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=non_existent_document,
        room=bed.room,
    )

    out = crud_hospitalization.add_hospitalization(new_hospitalization, db)
    assert out == 1

    new_hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        room=non_existent_bed,
    )

    document = random_document()
    new_user = schemas.UserCreate(
        num_document=document,
        rol="patient",
        password=random_password(10),
    )
    crud_admin.create_user(new_user, db)

    new_user.rol = "doctor"
    crud_admin.create_user(new_user, db)

    new_hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=document,
        num_doc_patient=document,
        room=bed.room,
    )

    out = crud_hospitalization.add_hospitalization(new_hospitalization, db)
    assert out == 3

    out = crud_hospitalization.add_hospitalization(new_hospitalization, db)
    assert out == 4

    new_hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        room=hospitalization.room,
    )

    out = crud_hospitalization.add_hospitalization(new_hospitalization, db)
    assert out == 5

    new_hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=hospitalization.num_doc_patient,
        room=bed.room,
    )

    out = crud_hospitalization.add_hospitalization(new_hospitalization, db)
    assert out == 6

    new_hospitalization = schemas.RegisterHospitalization(
        num_doc_doctor=doctor.num_document,
        num_doc_patient=patient.num_document,
        room=bed.room,
    )

    out = crud_hospitalization.add_hospitalization(new_hospitalization, db)
    assert out == 0


def test_discharge_hospitalization(db: Session) -> None:
    hospitalization: schemas.RegisterHospitalization = create_random_hospitalization(db)
    patient = create_random_patient(db)
    discharge_info = schemas.DischargeHospitalization(
        last_day=datetime.date.today() + datetime.timedelta(days=10)
    )

    out = crud_hospitalization.discharge_hospitalization(
        num_doc_patient=patient.num_document, discharge_info=discharge_info, db=db
    )
    assert out == 2

    discharge_info = schemas.DischargeHospitalization()
    out = crud_hospitalization.discharge_hospitalization(
        num_doc_patient=non_existent_document, discharge_info=discharge_info, db=db
    )
    assert out == 1

    out = crud_hospitalization.discharge_hospitalization(
        num_doc_patient=patient.num_document, discharge_info=discharge_info, db=db
    )
    assert out == 1

    out = crud_hospitalization.discharge_hospitalization(
        num_doc_patient=hospitalization.num_doc_patient,
        discharge_info=discharge_info,
        db=db,
    )
    assert out == 0

    out = crud_hospitalization.discharge_hospitalization(
        num_doc_patient=hospitalization.num_doc_patient,
        discharge_info=discharge_info,
        db=db,
    )
    assert out == 1
