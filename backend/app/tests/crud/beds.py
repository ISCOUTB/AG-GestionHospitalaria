import random

from sqlalchemy.orm import Session

from app import schemas
from app.crud import crud_bed

from app.tests.utils.hospitalizations import create_random_hospitalization
from app.tests.utils.bed import create_random_bed, non_existent_bed


def test_add_bed(db: Session) -> None:
    room = f"random_{random.choice(range(100))}"
    bed = schemas.BedBase(room=room)

    # Suponiendo que la cama no exista
    out = crud_bed.add_bed(bed, db)
    assert out == 0

    out = crud_bed.add_bed(bed, db)
    assert out == 1


def test_delete_bed(db: Session) -> None:
    hospitalization = create_random_hospitalization(db)
    bed = create_random_bed(db)

    out = crud_bed.delete_bed(non_existent_bed, db)
    assert out == 1

    out = crud_bed.delete_bed(hospitalization.room, db)
    assert out == 2

    out = crud_bed.delete_bed(bed.room, db)
    assert out == 0
