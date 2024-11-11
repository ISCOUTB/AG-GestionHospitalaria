import random

from sqlalchemy.orm import Session

from app.crud import crud_doctor
from app.schemas import DoctorAll, Speciality
from app.models import Specialities

from app.tests.utils.user import create_random_user


def create_random_speciality() -> Speciality:
    number = random.choices(range(0, 10), k=5)
    number_str = ''.join(str(x) for x in number)
    name = f"random_{number_str}"
    description = f"random description {number_str}"

    return Speciality(name=name, description=description)


def create_new_speciality(db: Session) -> Speciality:
    number = random.choices(range(0, 10), k=5)
    number_str = ''.join(str(x) for x in number)
    speciality = Speciality(
        name=f"random_{number_str}",
        description=f"random description {number_str}"
    )

    while (
        db.query(Specialities).filter(Specialities.name == speciality.name).first()
        is not None
    ):
        speciality = create_new_speciality(db)

    return speciality


def create_doctor_info(db: Session, k: int = 10) -> DoctorAll:
    user = create_random_user("doctor", db, k)
    speciality = create_random_speciality()

    out = crud_doctor.add_doctor_speciality(user.num_document, db, speciality)
    while out in (1, 2):
        speciality = create_random_speciality()
        out = crud_doctor.add_doctor_speciality(user.num_document, db, speciality)

    return crud_doctor.get_doctor(user.num_document, db)
