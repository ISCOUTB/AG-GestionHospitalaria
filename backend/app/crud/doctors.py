from typing import Literal

from app import models, schemas
from app.crud.base import CRUDBase

import sqlalchemy.exc
from sqlalchemy import select
from sqlalchemy.orm import Session


class CRUDDoctors(CRUDBase):
    def get_doctor(
        self, num_document: str, db: Session, active: bool = True
    ) -> schemas.DoctorAll | None:
        """
        Obtiene la información esencial de un doctor en particular

        Args:
            num_document (str): Número de documento del doctor que se desea encontrar.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            active (bool): Filtro de solo los doctores activos dentro del hospital. Por defecto `active=True`.

        Returns:
            schemas.DoctorAll: Retorna la información esencial y de las especialidades dado un doctor en particular.
            En caso de no encontrarlo, se retorna None
        """
        stmt = self.join_doctors(active).where(
            models.UsersInfo.num_document == num_document
        )
        query = db.execute(stmt).all()
        if not query:
            return None

        userbase: schemas.UserBase = self.create_user_base(query[0])
        specialities_list: list[schemas.SpecialityBase] = [
            schemas.SpecialityBase(name=x[-1]) for x in query if x[-1]
        ]

        return schemas.DoctorAll(
            **userbase.model_dump(), specialities=specialities_list
        )

    def get_doctors(self, db: Session, active: bool = True) -> list[schemas.DoctorAll]:
        """
        Obtiene la información de todos los doctores dentro del sistema

        Args:
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            active (bool): Filtro de solo los doctores activos dentro del hospital. Por defecto `active=True`.

        Returns:
            list[schemas.DoctorAll]: Se retorna una lista con la información esencial de los doctores
            y sus especialidades (incluye subespecialidades).
        """
        stmt = self.join_doctors(active)
        query = db.execute(stmt).all()
        results: list[schemas.DoctorAll] = []
        num_documents: set[str] = set(map(lambda row: row[0], query))
        for num_document in num_documents:
            data = list(filter(lambda row: row[0] == num_document, query))
            userbase: schemas.UserBase = self.create_user_base(data[0])
            specialities_list: list[schemas.SpecialityBase] = [
                schemas.SpecialityBase(name=x[-1]) for x in data if x[-1]
            ]

            results.append(
                schemas.DoctorAll(
                    **userbase.model_dump(), specialities=specialities_list
                )
            )

        return results

    def get_speciality_doctor(
        self, speciality: str, db: Session, active: bool = True
    ) -> list[schemas.DoctorAll]:
        """
        Obtiene todos los doctores los cuales tengan una especialidad especifica

        Args:
            speciality (str): Nombre de la especialidad por la que se quiere filtrar.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            active (bool): Filtra únicamente por los doctores que estén activos dentro del hospital. Por defecto `active=True`

        Returns:
            list[schemas.DoctorAll]: Retorna una lista con todos los doctores que tengan esa especialidad especificada.
        """
        stmt = self.join_doctors(active).where(models.Specialities.name == speciality)
        query = db.execute(stmt).all()
        num_documents = set(map(lambda row: row[0], query))

        return [
            self.get_doctor(num_document, db, active) for num_document in num_documents
        ]

    def get_specialities(self, db: Session) -> list[schemas.Speciality]:
        """
        Obtiene todas las especialidades de los doctores activos dentro del hospital

        Args:
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

        Returns:
            list[schemas.Speciality]: Retorna una lista con todas las especialidades que presentan los doctores activos dentro
            de la base de datos.
        """
        stmt = (
            select(models.Specialities.name, models.Specialities.description)
            .join(models.DoctorSpecialities)
            .join(models.UserRoles)
            .where(models.UserRoles.is_active == True)
        )

        query = set(db.execute(stmt).all())

        return list(
            map(
                lambda speciality: schemas.Speciality(
                    name=speciality[0], description=speciality[1]
                ),
                query,
            )
        )

    def add_doctor_speciality(
        self, num_document: str, db: Session, speciality: schemas.Speciality
    ) -> Literal[0, 1, 2, 3]:
        """
        Agrega una especialidad dado el número documento del doctor. Antes de agregar las especialidades, la información
        esencial del doctor tuvo que haber sido previamente creada. Además, el campo de `description` dentro de `speciality`
        no es necesario de agregar, únicamente cuando la especialidad no esté creada previamente en la base de datos

        Args:
            num_document (str): Número de documento del doctor.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            speciality (Speciality): Especialidad que se le agregará al doctor.

        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Estos son los posibles estados de la respuesta:
                - 0: Respuesta existosa
                - 1: Doctor no existente
                - 2: Especialidad no existente. Se debe completar el campo `description` dentro de `speciality`
                - 3: Relación de especialidad y doctor ya existente.
        """
        doctor_search: schemas.UserSearch = schemas.UserSearch(
            num_document=num_document, rol="doctor"
        )
        doctor: models.UserRoles | None = self.get_user_rol(doctor_search, db)
        if doctor is None:
            return 1

        current_specialities: list[schemas.Speciality] = self.get_specialities(db)
        speciality_exists: bool = any(
            map(lambda x: x.name == speciality.name, current_specialities)
        )

        if not speciality_exists and speciality.description is None:
            return 2

        if not speciality_exists:
            db.add(
                models.Specialities(
                    name=speciality.name, description=speciality.description
                )
            )

        speciality: models.Specialities = db.query(
            models.Specialities
        ).filter(models.Specialities.name == speciality.name).first()

        try:
            db.add(
                models.DoctorSpecialities(
                    doctor_id=doctor.id, speciality_id=speciality.id
                )
            )
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            return 3

        return 0

    def update_speciality(
        self, updated_speciality: schemas.Speciality, db: Session
    ) -> Literal[0, 1]:
        """
        Actualiza la descripción de una especialidad especificando su nombre

        Args:
            speciality (schemas.SpecialityBase): Especialidad que se quiere actualizar.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Estos son los posibles estados de la respuesta:
                - 0: Respuesta existosa.
                - 1: Especialidad no existe.
        """
        speciality: models.Specialities | None = db.query(models.Specialities) \
            .filter(models.Specialities.name == updated_speciality.name) \
            .first()

        if speciality is None:
            return 1
        
        speciality.description = updated_speciality.description
        db.commit()
        db.refresh(speciality)

        return 0


    def delete_speciality(
        self, num_document: str, speciality_name: schemas.SpecialityBase, db: Session
    ) -> Literal[0, 1, 2, 3]:
        """
        Elimina la especialidad de un doctor (no importa su estado) especificando su número de documento.

        Args:
            num_document (str): Número del documento del doctor.
            speciality (schemas.SpecialityBase): Especialidad del doctor que se quiere eliminar.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Los posibles estados de respuesta son:
                - 0: Resultado exitoso.
                - 1: Doctor inexistente.
                - 2: Especialidad inexistente.
                - 3: Relación inexistente.
        """
        doctor_search: schemas.UserSearch = schemas.UserSearch(
            num_document=num_document, rol="doctor"
        )
        doctor: models.UserRoles | None = self.get_user_rol(doctor_search, db, False)

        if doctor is None:
            return 1

        speciality: models.Specialities | None = (
            db.query(models.Specialities)
            .filter(models.Specialities.name == speciality_name.name)
            .first()
        )

        if speciality is None:
            return 2

        doctor_speciality: models.DoctorSpecialities | None = (
            db.query(models.DoctorSpecialities)
            .filter(
                models.DoctorSpecialities.doctor_id == doctor.id,
                models.DoctorSpecialities.speciality_id == speciality.id,
            )
            .first()
        )

        if doctor_speciality is None:
            return 3

        db.delete(doctor_speciality)
        db.commit()

        return 0


crud_doctor: CRUDDoctors = CRUDDoctors()
