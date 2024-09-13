from pydantic import BaseModel
from app.schemas.users import UserInfo


class ResponsablesInfo(BaseModel):
    responsable_num_doc: str | None = None
    responsable_type_doc: str | None = None
    responsable_name: str | None = None
    responsable_surname: str | None = None
    responsable_relationship: str | None = None


class PatientInfo(UserInfo, ResponsablesInfo):
    rol = "patient"
