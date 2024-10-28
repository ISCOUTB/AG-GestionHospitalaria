from sqlalchemy.orm import Session

from app.tests.utils.user import create_random_user
from app.tests.utils.doctor import (
    create_random_speciality,
    create_doctor_info,
    create_new_speciality,
)
from app.tests.utils.user import non_existent_document

from app import schemas
from app.crud import crud_doctor


def test_get_doctor(db: Session) -> None:
    doctor_in = crud_doctor.get_doctor(non_existent_document, db)
    assert doctor_in is None

    doctor = create_doctor_info(db)
    doctor_in = crud_doctor.get_doctor(doctor.num_document, db)
    assert doctor.num_document == doctor_in.num_document
    assert doctor.specialities == doctor_in.specialities


def test_add_doctor_speciality(db: Session) -> None:
    speciality = schemas.Speciality(name="")
    out = crud_doctor.add_doctor_speciality(non_existent_document, db, speciality)
    assert out == 1

    doctor = create_random_user("doctor", db, 10)
    speciality = create_new_speciality(db)
    out = crud_doctor.add_doctor_speciality(doctor.num_document, db, speciality)
    assert out == 2

    speciality = create_random_speciality()
    out = crud_doctor.add_doctor_speciality(doctor.num_document, db, speciality)
    assert out == 0

    out = crud_doctor.add_doctor_speciality(doctor.num_document, db, speciality)
    assert out == 3


def test_delete_speciality(db: Session) -> None:
    speciality = schemas.SpecialityBase(name="")
    out = crud_doctor.delete_speciality(non_existent_document, speciality, db)
    assert out == 1

    doctor = create_doctor_info(db)
    speciality.name = create_new_speciality(db).name
    out = crud_doctor.delete_speciality(doctor.num_document, speciality, db)
    assert out == 2

    speciality = doctor.specialities[0]
    out = crud_doctor.delete_speciality(doctor.num_document, speciality, db)
    assert out == 0

    out = crud_doctor.delete_speciality(doctor.num_document, speciality, db)
    assert out == 3
