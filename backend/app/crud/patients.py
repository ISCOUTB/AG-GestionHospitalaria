from typing import Literal

from app import models, schemas
from app.crud.base import CRUDBase

import sqlalchemy.exc
from sqlalchemy.orm import Session


class CRUDPatients(CRUDBase):
    def get_patients(self, db: Session, active: bool = True) -> list[schemas.PatientAll]:
        """
        Obtiene todos los pacientes que están dentro del sistema 
        
        Args:
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            active (bool): Filtra únicamente por los usuarios que estén activos dentro del hospital. Por defecto `active=True`.
        
        Returns:
            list[schemas.PatientAll]: Retorna una lista con la información de todos los pacientes junto a la de sus responsables.
        """
        stmt = self.join_patients(active)
        query = db.execute(stmt).all()
        results: list[schemas.PatientAll] = []
        for row in query:
            userbase = self.create_user_base(row[:9])
            responsable_info = self.create_patient_info(row[9:])
            results.append(schemas.PatientAll(
                **userbase.model_dump(),
                **responsable_info.model_dump()
            ))
        
        return results
    
    def get_patient(self, num_document: str, db: Session, active: bool = True) -> schemas.PatientAll | None:
        """
        Obtiene toda la información de un paciente especificando su número de documento

        Args:
            num_document (str): Número de documento del paciente que se desea obtener
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            active (bool): Filtra únicamente por todos los pacientes que estén activos en el hospital. Por defecto `active=True`.

        Returns:
            schemas.PatientAll | None: Retorna toda la información detallada de un paciente, junto a la de su responsable. En caso
            del paciente no encontrarse, se retorna `None`.
        """
        stmt = self.join_patients(active).where(models.UsersInfo.num_document == num_document)
        query = db.execute(stmt).first()
        if not query:
            return None

        userbase = self.create_user_base(query[:9])
        responsable_info = self.create_patient_info(query[9:])
        return schemas.PatientAll(
            **userbase.model_dump(),
            **responsable_info.model_dump()
        )
    
    def add_responsable(self, num_document: str, responsable_info: schemas.ResponsablesInfo, db: Session) -> Literal[0, 1, 2, 3, 4]:
        """
        Agrega la información del responsable de un paciente determinado que esté activo dentro del hospital

        Args:
            num_document (str): Número de documento paciente que se le agregará la información del responsable.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            responsable_info (str): Información del responsable para el paciente determinado.
        
        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Estos son los posibles estados de la respuesta:
                - 0: Respuesta existosa.
                - 1: Paciente no existente.
                - 2: El paciente no puede ser su propio responsable.
                - 3: El responsable no puede tener el mismo documento que algun paciente activo dentro del hospital.
                - 4: Información del responsable para ese paciente ya existente.
        """
        valid_responsable: int = self.valid_responsable_doc(num_document, responsable_info.num_doc_responsable, db)
        if valid_responsable != 0:
            return valid_responsable

        patient_search: schemas.UserSearch = schemas.UserSearch(num_document=num_document, rol='patient')
        patient: models.UserRoles | None = self.get_user_rol(patient_search, db)

        if patient is None:
            return 1

        responsable: models.PatientInfo = models.PatientInfo(
            patient_id=patient.id,
            **responsable_info
        )

        try:
            db.add(responsable)
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            return 4
        
        return 0

    def update_patient(self, num_document: str, updated_info: schemas.ResponsablesInfo, db: Session) -> Literal[0, 1, 2, 3, 4]:
        """
        Actualiza la información del responsable dado un determinado paciente sin importar su estado dentro del sistema

        Args:
            num_document (str): Número de documento del paciente al que se le editará la información.
            updated_info (schemas.ResponsablesInfo): Información que se actualizará al responsable del paciente.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Estos son los posibles estados de la respuesta:
                - 0: Respuesta existosa.
                - 1: Paciente inexistente.
                - 2: El paciente no puede ser su propio responsable.
                - 3: El responsable no puede ser otro paciente activo dentro del hospital.
                - 4: Información previa del responsable no existente.
        """
        if updated_info.num_doc_responsable is not None and \
            (out := self.valid_responsable_doc(num_document, updated_info.num_doc_responsable, db)) != 0:
            return out
        
        patient_search: schemas.UserSearch = schemas.UserSearch(num_document=num_document, rol='patient')
        patient: models.UserRoles | None = self.get_user_rol(patient_search, db, False)
        
        if patient is None:
            return 1
        
        responsable: models.PatientInfo | None = db.query(models.PatientInfo).filter(
            models.PatientInfo.patient_id == patient.id).first()
        
        if responsable is None:
            return 4
        
        if updated_info.num_doc_responsable is not None:
            responsable.num_doc_responsable = updated_info.num_doc_responsable
        
        if updated_info.type_doc_responsable is not None:
            responsable.type_doc_responsable = updated_info.type_doc_responsable

        if updated_info.name_responsable is not None:
            responsable.name_responsable = updated_info.type_doc_responsable

        if updated_info.surname_responsable is not None:
            responsable.surname_responsable = updated_info.type_doc_responsable

        if updated_info.phone_responsable is not None:
            responsable.phone_responsable = updated_info.phone_responsable
        
        if updated_info.relationship_responsable is not None:
            responsable.relationship_responsable = updated_info.phone_responsable
        
        db.commit()
        db.refresh(responsable)

        return 0
    
    def delete_responsable(self, num_document: str, db: Session) -> Literal[0, 1, 2]:
        """
        Elimina la información del responsable dado un determinado paciente sin importar su estado dentro del sistema.

        Args:
            num_document (str): Número de documento del paciente al que se le editará la información.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Estos son los posibles estados de la respuesta:
                - 0: Respuesta existosa.
                - 1: Paciente inexistente.
                - 2: Información previa del responsable no existente.
        """
        patient_search: schemas.UserSearch = schemas.UserSearch(num_document=num_document, rol='patient')
        patient: models.UserRoles | None = self.get_user_rol(patient_search, db, False)
        
        if patient is None:
            return 1
        
        responsable: models.PatientInfo | None = db.query(models.PatientInfo).filter(
            models.PatientInfo.patient_id == patient.id).first()
        
        if responsable is None:
            return 2

        db.delete(responsable)
        db.commit()

        return 0


crud_patient: CRUDPatients = CRUDPatients()
