import random

from sqlalchemy.orm import Session

from app.crud import crud_doctor
from app.schemas import DoctorAll, Speciality
from app.models import Specialities

from app.tests.utils.user import create_random_user


def create_random_speciality() -> Speciality:
    number = random.choice(range(100))
    name = f'random_{number}'
    description = f'random description {number}'

    return Speciality(name=name, description=description)


def create_new_speciality(db: Session) -> Speciality:
    number = random.choices(range(1000), k=3)
    speciality = Speciality(name=f'random_{number}')

    while db.query(Specialities).filter(
        Specialities.name == speciality.name).first() is not None:
        speciality = create_new_speciality(db)
    
    return speciality


def create_doctor_info(db: Session, k: int = 10) -> DoctorAll:
    user = create_random_user('doctor', db, k)
    speciality = create_random_speciality()

    out = crud_doctor.add_doctor_speciality(user.num_document, db, speciality)
    while out == 3:
        speciality = create_random_speciality()
        out = crud_doctor.add_doctor_speciality(user.num_document, db, speciality)

    return crud_doctor.get_doctor(user.num_document, db)    
