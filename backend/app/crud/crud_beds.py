from typing import Literal

from app import models, schemas
from app.crud.crud_base import CRUDBase

import sqlalchemy.exc
from sqlalchemy import select
from sqlalchemy.orm import Session, aliased


class CRUDBeds(CRUDBase):
    def get_beds(self, db: Session, all: bool = False) -> list[schemas.models.Beds] | list[schemas.BedAll]:
        """
        Obtiene un listado con todas las camas del hospital

        Args:
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            all (bool): Especifica si además quiere que se muestre la información acerca del uso de la cama.
                Por defecto, `all=False`.
        Returns:
            list: Retorna una lista de las camas, dependiendo del paramétro `all` se retornará una lista de `schemas.BedBase` (cuando `all=False`) o
                `schemas.BedAll` (cuando `all=True`). 
        """
        if not all:
            return list(map(lambda bed: schemas.models.Beds.model_validate(bed), 
                            db.query(models.Beds).all()))
        
        stmt = self.join_beds()
        results = db.execute(stmt).all()

        return list(map(lambda row: schemas.BedAll(
            room=row[0], num_doc_patient=row[1], num_doc_doctor=row[2]
            ), results))
    
    def add_bed(self, bed_info: schemas.BedBase, db: Session) -> Literal[0, 1]:
        """
        Agrega una nueva cama al hospital al hospital especificando el cuarto

        Args:
            room (schemas.BedBase): Información de la nueva cama que se agregará al hospital.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Los posibles estados de respuesta son:
                - 0: Respuesta exitosa. La cama fue agregada a la base de datos perfectamente
                - 1: El cuarto de la cama ya se encuentra repetida en la base de datos
        """
        try:
            db.add(models.Beds(room=bed_info.room))
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            return 1

        return 0
    
    def delete_bed(self, room: str, db: Session) -> Literal[0, 1, 2]:
        """
        Elimina una cama dentro del hospital que no esté en uso, especificando el cuarto donde esté

        Args:
            room (str): Habitación de la cama que se desea eliminar del sistema.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Los posibles estados de respuesta son:
                - 0: Resultado exitoso.
                - 1: Habitación inexistente.
                - 2: Cama en uso.
        """
        bed: models.Beds | None = db.query(models.Beds).filter(
            models.Beds.room == room
        ).first()

        if bed is None:
            return 1
        
        stmt = select(models.BedsUsed).where(models.BedsUsed.id_bed == bed.id)
        if not db.execute(stmt).first():
            return 2
        
        db.delete(bed)
        db.commit()

        return 0


crud_bed: CRUDBeds = CRUDBeds()
