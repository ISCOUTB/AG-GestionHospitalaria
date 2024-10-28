import datetime
from typing import Literal

from app import models, schemas
from app.crud.base import CRUDBase

from sqlalchemy import select
from sqlalchemy.orm import Session, aliased


class CRUDHospitalizations(CRUDBase):
    def get_hospitalizations(self, db: Session) -> list[schemas.Hospitalization]:
        """
        Obtiene una lista con el historial de hospitalizaciones en el hospital

        Args:
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

        Returns:
            list[schemas.Hospitalizations]: Retorna una lista con todas las hospitalizaciones
        """
        doctor = aliased(models.UserRoles)
        patient = aliased(models.UserRoles)

        stmt = select(
            patient.num_document,
            doctor.num_document,
            models.Hospitalizations.entry_day,
            models.Hospitalizations.last_day
        ).join(doctor, doctor.id == models.Hospitalizations.id_doctor) \
        .join(patient, patient.id == models.Hospitalizations.id_patient)

        result = db.execute(stmt).all()

        return list(map(lambda row: schemas.Hospitalization(
            num_doc_patient=row[0], num_doc_doctor=row[1],
            entry_day=row[2], last_day=row[3]
        ), result))
    
    def add_hospitalization(self, hospitalization_info: schemas.RegisterHospitalization, db: Session) -> Literal[0, 1, 2, 3, 4, 5]:
        """
        Agrega una nueva hospitalización a la base de datos

        Args:
            hospitalization_info (schemas.RegisterHospitalization): Información de la hospitalización.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
        
        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Los posibles estados de respuesta son:
                - 0: Resultado exitoso.
                - 1: Paciente no existente.
                - 2: Doctor no existente.
                - 3: Cama no existente.
                - 4: Cama en uso.
                - 5: Paciente ya en cama
        """
        # Realizar las validaciones
        if isinstance(out := self.valid_basic_appointment(hospitalization_info, db), int):
            return out

        patient, doctor = out

        bed: models.Beds | None = db.query(models.Beds).filter(
            models.Beds.room == hospitalization_info.room
        ).first()
        if bed is None:
            return 3
        
        if bed in db.execute(select(models.BedsUsed.id_bed)).all():
            return 4

        if patient.id in db.execute(select(models.BedsUsed.id_patient)).all():
            return 5

        # Ocupar la cama
        bed_used: models.BedsUsed = models.BedsUsed(id_bed=bed.id,
                                                    id_patient=patient.id,
                                                    id_doctor=doctor.id)
        db.add(bed_used)

        # Agregar la hospitalización
        hospitalization: models.Hospitalizations = models.Hospitalizations(id_patient=patient.id,
                                                                           id_doctor=doctor.id,
                                                                           entry_day=hospitalization_info.entry_day)
        db.add(hospitalization)
        db.commit()
        return 0
    
    def discharge_hospitalization(self, num_doc_patient: str, discharge_info: schemas.DischargeHospitalization, db: Session) -> Literal[0, 1, 2]:
        """
        Da el alta a un determinado paciente que esté actualmente hospitalizado

        Args:
            num_doc_patient (str): Número de documento del paciente que se le dará el alta.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            discharge_info (schemas.DischargeHospitalization): Día el cual se le da el alta. Por defecto, la fecha es la actual

        Returns: 
            int: Retorna un entero simbolizando el estado de la respuesta. Estos son los posibles estados de la respuesta:
                - 0: Respuesta existosa.
                - 1: Paciente hospitalizado no encontrado.
                - 2: Mal formato de fecha. Aplica cuando la fecha es mayor que el día actual o menor a la fecha de hospitalización
        """
        hospitalization: models.Hospitalizations | None = db.query(models.Hospitalizations).filter(
            models.Hospitalizations.id_patient == num_doc_patient, models.Hospitalizations.last_day is None
        ).first()

        if hospitalization is None:
            return 1
        
        if not hospitalization.entry_day <= discharge_info.last_day <= datetime.date.today():
            return 2

        # Dar de alta al paciente actualizando la fecha
        hospitalization.last_day = discharge_info.last_day

        # Eliminar cama
        patient: models.UserRoles = db.query(models.UserRoles).filter(models.UserRoles.num_document == num_doc_patient).first()
        bed_used: models.BedsUsed = db.query(models.BedsUsed).filter(models.BedsUsed.id_patient == patient.id).first()
        db.delete(bed_used)

        db.commit()
        db.refresh(hospitalization)

        return 0


crud_hospitalization: CRUDHospitalizations = CRUDHospitalizations()
