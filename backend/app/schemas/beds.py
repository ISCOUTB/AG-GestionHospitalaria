from pydantic import BaseModel


class BedBase(BaseModel):
    room: str


class UseBed(BedBase):
    num_doc_doctor: str
    num_doc_patient: str


class VacateBed(BedBase):
    pass
