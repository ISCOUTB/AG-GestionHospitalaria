import random

from sqlalchemy.orm import Session

from app.crud import crud_bed
from app.schemas import BedBase


non_existent_bed = "NonExistentBed"


def random_bed() -> BedBase:
    room = f"random_bed{random.choice(range(1_000_000))}"
    return BedBase(room=room)


def create_random_bed(db: Session) -> BedBase:
    bed = random_bed()
    out = crud_bed.add_bed(bed, db)

    while out == 1:
        bed = random_bed()
        out = crud_bed.add_bed(bed, db)

    return bed
