from pydantic import BaseModel
from app.schemas.users import Roles


class TokenPayload(BaseModel):
    number_document: str
    rol: Roles


class Token(BaseModel):
    access_token: str
    token_type: str
