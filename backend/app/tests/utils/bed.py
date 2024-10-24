import random

from sqlalchemy.orm import Session

from app.crud import crud_bed
from app.schemas import BedBase


non_existent_bed = 'NonExistentBed'

def create_random_bed(db: Session) -> BedBase:
    room = f'random_bed{random.choice(range(100))}'
    bed = BedBase(room=room)
    out = crud_bed.add_bed(bed, db)

    while out == 1:
        room = f'random_bed{random.choice(range(100))}'
        out = crud_bed.add_bed(bed, db)

    return bed
