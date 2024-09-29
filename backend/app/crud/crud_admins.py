import datetime

from app import models, schemas
from app.crud.crud_users import CRUDUsers


from app.core.security import get_password_hash

import sqlalchemy.exc
from sqlalchemy import select
from sqlalchemy.orm import Session


class CRUDAdmins(CRUDUsers):
    def create_user(self, new_user: schemas.UserCreate, db: Session, admins: bool = False) -> int:
        """
        Crea un nuevo usuario en el sistema. Esta operación es únicamente reservada para los administradores del sistema,
        y, en caso de querer agregar un administrador, solo lo podría realizar el superusuario.
        
        Para los usuarios que no estén previamente agregados en el sistema, se les creará su espacio sin problemas. Ahora,
        si sí está el usuario con ese rol en el sistema como inactivo, únicamente cambiará de estado, en otro caso, no se
        podrá realizar la operación

        Args:
            new_admin (UserCreate): Información del nuevo administrador.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            admins (bool): Válida si se quiere agregar la información de algún administrador.

        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Estos son los posibles estados de la respuesta:
                - 0: Respuesta existosa
                - 1: El usuario es administrador, no se puede editar. Solo aparece cuando `admins=False`.
                - 2: Usuario activo con mismo número de documento
        """
        if not admins and new_user.rol == 'admin':
            return 1

        user: schemas.UserAll = self.get_user(new_user.num_document, db, rol=True, active=False)

        # Crear la información del usuario si no existe en el sistema
        if user is None:
            user_info: models.UsersInfo = models.UsersInfo(
                num_document=new_user.num_document,
                type_document=new_user.type_document,
                name=new_user.name,
                surname=new_user.surname,
                sex=new_user.sex,
                birthday=new_user.birthday,
                address=new_user.address,
                phone=new_user.phone,
                email=new_user.email
            )

            db.add(user_info)

        user_rol: models.UserRoles | None = self.get_user_rol(schemas.UserSearch(
            num_document=new_user.num_document, rol=new_user.rol
        ), db, False)
        
        # Crear el usuario para ese rol en caso de no existir
        if user_rol is None:
            new_user_rol = models.UserRoles(
                num_document=new_user.num_document,
                rol=new_user.rol,
                password=get_password_hash(new_user.password),
                is_active=True
            )
            db.add(new_user_rol)
            db.commit()

            return 0
        
        # Si el usuario ya existe y está activo, retornar el aviso
        if user_rol.is_active == True:
            return 2
        
        user_rol.is_active = True
        db.commit()
        db.refresh(user_rol)

        return 0

    def update_user(self, num_document: str, updated_info: schemas.UserBase, db: Session, admins: bool = False) -> int:
        """
        Actualiza la información completa de cualquier usuario dentro del sistema sin importar su estado actual (activo o no).

        Args:
            num_document (str): Número de documento del usuario a modificar.
            updated_info (UserUpdate): Información que se quiere actualizar. Si no se quiere actualizar el número de documento,
                dejarlo como `''`.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            admins (bool): Válida si se quiere actualizar la información de algún administrador.

        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Los posibles estados de respuesta son:
                - 0: Resultado exitoso.
                - 1: Número de documento inexistente.
                - 2: El usuario es administrador, no se puede editar. Solo aparece cuando `admins=False`.
                - 3: Número de documento repetido.
        """
        user: schemas.UserAll = self.get_user(num_document, db, rol=True, active=False)
        
        if user is None:
            return 1
        
        if not admins and 'admin' in list(map(lambda pair: pair[0], user.roles)):
            return 2

        user_info: models.UsersInfo = db.query(models.UsersInfo).filter(models.UsersInfo.num_document == num_document).first()

        if updated_info.num_document:
            user_info.num_document = updated_info.num_document
        
        if updated_info.type_document is not None:
            user_info.type_document = updated_info.type_document

        if updated_info.name is not None:
            user_info.name = updated_info.name
        
        if updated_info.surname is not None:
            user_info.surname = updated_info.surname

        if updated_info.sex is not None:
            user_info.sex = updated_info.sex

        if updated_info.birthday is not None:
            user_info.birthday = updated_info.birthday
        
        if updated_info.address is not None:
            user_info.address = updated_info.address
        
        if updated_info.phone is not None:
            user_info.phone = updated_info.phone
        
        if updated_info.email is not None:
            user_info.email = updated_info.email
        
        try:
            db.commit()
            db.refresh(user_info)
        except sqlalchemy.exc.IntegrityError:
            return 3
        
        return 0
    
    def delete_user(self, num_document: str, rol: schemas.Roles, db: Session, admin: bool = False) -> int:
        """
        "Elimina" a un usuario activo dentro del sistema. En realidad, lo que se hace es colocar al usuario como inactivo.
        En el caso de los pacientes que están en cama, no se pueden colocar como inactivos todavía.

        Args:
            num_document (str): Número de documento del usuario que se va a "eliminar".
            rol (schemas.Roles): Se especifica el rol el cual se va a "eliminar". Únicamente puede ser doctores o pacientes.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            admin (bool): Especifica si es posible eliminar un administrador dentro de la base de datos. Por defecto, `admin=False`.
        
        Returns:
            int: Retorna un entero simbolizando el estado de la respuesta. Los posibles estados de respuesta son:
                - 0: Resultado exitoso.
                - 1: Usuario inexistente.
                - 2: El usuario es administrador, no se puede eliminar. Solo aparece cuando `admin=False` y `rol='admin'`.
                - 3: Paciente que está en cama
        """
        if rol == 'admin' and not admin:
            return 2
        
        user_search: schemas.UserSearch = schemas.UserSearch(num_document=num_document, rol=rol)
        user: models.UserRoles | None = self.get_user_rol(user_search, db)

        if user is None:
            return 1
        
        if rol == 'patient':
            stmt = select(models.BedsUsed.id_patient).where(user.id == models.BedsUsed.id_patient)
            if not db.execute(stmt):
                return 3

        user.is_active = False
        user.inactivity = datetime.date.today()

        db.commit()
        db.refresh(user)

        return 0


crud_admin = CRUDAdmins()