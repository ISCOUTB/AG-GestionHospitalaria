from pydantic import BaseModel


class AddSpeciality(BaseModel):
    number_document: str  # Número de documento del doctor
    name: str
    description: str
