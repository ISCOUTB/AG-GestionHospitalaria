from typing import Literal, Any

from app import models, schemas

from sqlalchemy import select
from sqlalchemy.orm import Session, aliased


class CRUDBase:
    def join_users(self, active: bool = True):
        stmt = select(
            models.UsersInfo.num_document,
            models.UsersInfo.type_document,
            models.UsersInfo.name,
            models.UsersInfo.surname,
            models.UsersInfo.sex,
            models.UsersInfo.birthday,
            models.UsersInfo.address,
            models.UsersInfo.phone,
            models.UsersInfo.email,
            models.UserRoles.rol,
            models.UserRoles.is_active,
        ).join(models.UserRoles)
        if active:
            stmt = stmt.where(models.UserRoles.is_active == True)

        return stmt

    def join_beds(self):
        doctor = aliased(models.UserRoles)
        patient = aliased(models.UserRoles)

        stmt = (
            select(models.Beds.room, patient.num_document, doctor.num_document)
            .join(
                models.BedsUsed, models.BedsUsed.id_bed == models.Beds.id, isouter=True
            )
            .join(doctor, doctor.id == models.BedsUsed.id_doctor, isouter=True)
            .join(patient, patient.id == models.BedsUsed.id_patient, isouter=True)
        )

        return stmt

    def create_user_base(self, data: list[Any]) -> schemas.UserBase:
        return schemas.UserBase(
            num_document=data[0],
            type_document=data[1],
            name=data[2],
            surname=data[3],
            sex=data[4],
            birthday=data[5],
            address=data[6],
            phone=data[7],
            email=data[8],
        )

    def join_doctors(self, active: bool = True):
        stmt = (
            select(
                models.UsersInfo.num_document,
                models.UsersInfo.type_document,
                models.UsersInfo.name,
                models.UsersInfo.surname,
                models.UsersInfo.sex,
                models.UsersInfo.birthday,
                models.UsersInfo.address,
                models.UsersInfo.phone,
                models.UsersInfo.email,
                models.UserRoles.is_active,
                models.Specialities.name,
            )
            .join(
                models.UserRoles,
                models.UserRoles.num_document == models.UsersInfo.num_document,
            )
            .join(models.DoctorSpecialities, isouter=True)
            .join(models.Specialities, isouter=True)
        ).where(models.UserRoles.rol == "doctor")
    
        if active:
            stmt = stmt.where(models.UserRoles.is_active == True)

        return stmt

    def join_patients(self, active: bool = True):
        stmt = (
            select(
                models.UsersInfo.num_document,
                models.UsersInfo.type_document,
                models.UsersInfo.name,
                models.UsersInfo.surname,
                models.UsersInfo.sex,
                models.UsersInfo.birthday,
                models.UsersInfo.address,
                models.UsersInfo.phone,
                models.UsersInfo.email,
                models.PatientInfo.num_doc_responsable,
                models.PatientInfo.type_doc_responsable,
                models.PatientInfo.name_responsable,
                models.PatientInfo.surname_responsable,
                models.PatientInfo.phone_responsable,
                models.PatientInfo.relationship_responsable,
            )
            .join(
                models.UserRoles,
                models.UsersInfo.num_document == models.UserRoles.num_document,
            )
            .join(models.PatientInfo, isouter=True)
        )

        if active:
            stmt = stmt.where(models.UserRoles.is_active == True)

        return stmt.where(models.UserRoles.rol == "patient")

    def create_patient_info(self, data: list[Any]) -> schemas.ResponsablesInfo:
        return schemas.ResponsablesInfo(
            num_doc_responsable=data[0],
            type_doc_responsable=data[1],
            name_responsable=data[2],
            surname_responsable=data[3],
            phone_responsable=data[4],
            relationship_responsable=data[5],
        )

    def valid_basic_appointment(
        self, info: schemas.BaseAppointment, db: Session
    ) -> Literal[1, 2] | tuple[models.UserRoles]:
        patient_search: schemas.UserSearch = schemas.UserSearch(
            num_document=info.num_doc_patient, rol="patient"
        )

        doctor_search: schemas.UserSearch = schemas.UserSearch(
            num_document=info.num_doc_doctor, rol="doctor"
        )

        patient: models.UserRoles | None = self.get_user_rol(patient_search, db)
        if patient is None:
            return 1

        doctor: models.UserRoles | None = self.get_user_rol(doctor_search, db)
        if doctor is None:
            return 2

        return patient, doctor

    def get_user_rol(
        self, user_search: schemas.UserSearch, db: Session, active: bool = True
    ) -> models.UserRoles | None:
        """
        Obtiene directamente una instancia de un usuario de la tabla de los roles de los usuarios

        Args:
            user_search (schemas.UserSearch): Información de usuario para buscar en la base de datos.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            active (bool): Limitación de querer solo un usuario que esté activo. Por defecto, `active=True`.

        Returns:
            models.UserRoles | None: Retorna un objeto `models.UserRoles` si existe, en caso contrario retorna `None`.
        """
        conditions = [
            models.UserRoles.num_document == user_search.num_document,
            models.UserRoles.rol == user_search.rol,
        ]
        if active:
            conditions.append(models.UserRoles.is_active == True)

        return db.query(models.UserRoles).filter(*conditions).first()

    def get_user_info(self, num_document: str, db: Session) -> models.UsersInfo | None:
        """
        Obtiene directamente una instancia de un usuario dentro de la tabla con la información de los usuarios

        Args:
            num_document (str): Número de documento del usuario a buscar.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

        Returns:
            models.UsersInfo | None: Retorna una objeto `models.UsersInfo` si existe, en caso contrario retorna `None`.
        """
        return (
            db.query(models.UsersInfo)
            .filter(models.UsersInfo.num_document == num_document)
            .first()
        )


if __name__ == "__main__":
    crud_base = CRUDBase()

    print(crud_base.join_users())
