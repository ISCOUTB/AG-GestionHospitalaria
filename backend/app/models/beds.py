import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import BaseModel


class Beds(BaseModel):
    __tablename__ = "beds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room = Column(
        String, nullable=False, unique=True
    )  # Esto es básicamente una llave primaria
    # Se le pueden seguir agregando otros atributos en caso de de ser necesario

    beds_used = relationship(
        "BedsUsed",
        uselist=False,
        back_populates="beds",
        passive_deletes=True,
        passive_updates=True,
    )
