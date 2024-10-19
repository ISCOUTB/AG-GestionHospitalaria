from app import models, schemas
from app.crud.base import CRUDBase

from sqlalchemy import select
from sqlalchemy.orm import Session, aliased


class CRUDConsultatations(CRUDBase):
    def get_consultations(self, db: Session) -> list[schemas.Consultation]:
        """
        Obtiene una lista con el historial de consultas médicas en el hospital
        
        Args:
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

        Returns:
            list[schemas.Consultation]: Retorna una lista con todas las consultas médicas
        """
        doctor = aliased(models.UserRoles)
        patient = aliased(models.UserRoles)

        stmt = select(
            patient.num_document,
            doctor.num_document,
            models.MedicalConsults.area,
            models.MedicalConsults.day
        ).join(doctor, doctor.id == models.MedicalConsults.id_doctor) \
        .join(patient, patient.id == models.MedicalConsults.id_patient)

        result = db.execute(stmt).all()

        return list(map(lambda row: schemas.Consultation(
            num_doc_patient=row[0], num_doc_doctor=row[1],
            area=row[2], day=row[3]
        ), result))
    
    def add_consultation(self, consultation_info: schemas.Consultation, db: Session) -> int:
        """
        Agrega una nueva consulta médica a la base de datos

        Args:
            consultation_info (schemas.Consultation): Información de la consulta médica.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
        
        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Los posibles estados de respuesta son:
                - 0: Resultado exitoso.
                - 1: Paciente no existente.
                - 2: Doctor no existente.
        """
        # Realizar las validaciones
        if isinstance(out := self.valid_basic_appointment(consultation_info), int):
            return out

        patient, doctor = out

        consultation: models.MedicalConsults = models.MedicalConsults(
            id_patient=patient.id,
            id_doctor=doctor.id,
            area=consultation_info.area,
            day=consultation_info.day
        )

        db.add(consultation)
        db.commit()

        return 0


crud_consultation: CRUDConsultatations = CRUDConsultatations()
