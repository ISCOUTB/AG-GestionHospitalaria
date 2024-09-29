from app import models, schemas

from sqlalchemy import select
from sqlalchemy.orm import Session, aliased


class CRUDBase:
    def __join_users(self, active: bool = True):
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

    def __join_beds(self):
        doctor = aliased(models.UserRoles)
        patient = aliased(models.UserRoles)

        stmt = select(
            models.Beds.room,
            patient.num_document,
            doctor.num_document
        ).join(models.BedsUsed, models.BedsUsed.id_bed == models.Beds.id, isouter=True) \
        .join(doctor, doctor.id == models.BedsUsed.id_doctor, isouter=True) \
        .join(patient, patient.id == models.BedsUsed.id_patient, isouter=True)

        return stmt

    def __create_user_base(self, data: list[any]) -> schemas.UserBase:
        return schemas.UserBase(
            num_document=data[0],
            type_document=data[1],
            name=data[2],
            surname=data[3],
            sex=data[4],
            birthday=data[5],
            address=data[6],
            phone=data[7],
            email=data[8]
        )

    def __join_doctors(self, active: bool = True):
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
            models.UserRoles.is_active,
            models.Specialities.name,
        ).join(models.UserRoles, models.UserRoles.num_document == models.UsersInfo.num_document) \
        .join(models.DoctorSpecialities, isouter=True) \
        .join(models.Specialities)

        if active:
            stmt.where(models.UserRoles.is_active == True)

        return stmt
    
    def __join_patients(self, active: bool = True):
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
            models.PatientInfo.num_doc_responsable,
            models.PatientInfo.type_doc_responsable,
            models.PatientInfo.name_responsable,
            models.PatientInfo.surname_responsable,
            models.PatientInfo.phone_responsable,
            models.PatientInfo.relationship_responsable
        ).join(models.UserRoles, models.UsersInfo.num_document == models.UserRoles.num_document) \
        .join(models.PatientInfo, isouter=True)
        
        if active:
            stmt = stmt.where(models.UserRoles.is_active == True)

        return stmt.where(models.UserRoles.rol == 'patient')
    
    def __create_patient_info(self, data: list[any]) -> schemas.ResponsablesInfo:
        return schemas.ResponsablesInfo(
            num_doc_responsable=data[0],
            type_doc_responsable=data[1],
            name_responsable=data[2],
            surname_responsable=data[3],
            phone_responsable=data[4],
            relationship_responsable=data[5]
        )

    def __valid_responsable_doc(self, patient_doc: str, responsable_doc: str, db: Session) -> int:
        """
        Válida que el número de documento de un responsable pueda ser utilizable

        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Estos son los posibles estados de la respuesta:
                - 0: Puede ser utilizado.
                - 2: El paciente es su propio responsable. No se puede.
                - 3: El responsable tiene el mismo documento que algun paciente activo dentro del hospital. No se puede
        """
        
        if patient_doc == responsable_doc:
            return 2
        
        if responsable_doc in list(map(
            lambda patient: patient.num_document, self.get_all_patients(db)
        )):
            return 3

        return 0

    def __valid_basic_appointment(self, info: schemas.BaseAppointment, db: Session) -> int | tuple[models.UserRoles]:
        patient_search: schemas.UserSearch = schemas.UserSearch(
            num_document=info.num_doc_patient,
            rol='patient'
        )

        doctor_search: schemas.UserSearch = schemas.UserSearch(
            num_document=info.num_doc_doctor,
            rol='doctor'
        )
        
        patient: models.UserRoles | None = self.get_user_rol(patient_search, db)
        if patient is None:
            return 1

        doctor: models.UserRoles | None = self.get_user_rol(doctor_search, db)
        if doctor is None:
            return 2
        
        return patient, doctor
    
    def get_user_rol(self, user_search: schemas.UserSearch, db: Session, active: bool = True) -> models.UserRoles | None:
        """
        Obtiene directamente un instancia de la tabla de los roles de los usuarios

        Args:
            user_search: Información de usuario para buscar en la base de datos.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            active (bool): Limitación de querer solo un usuario que esté activo. Por defecto, `active=True`. 
        
        Returns:
            models.UserRoles | None: Retorna un objeto `models.UserRoles` si existe, en caso contrario retorna `None`.
        """
        conditions = [models.UserRoles.num_document == user_search.num_document, models.UserRoles.rol == user_search.rol]
        if active:
            conditions.append(models.UserRoles.is_active == True)
        
        return db.query(models.UserRoles).filter(*conditions).first()