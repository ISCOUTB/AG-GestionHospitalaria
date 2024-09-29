from app import models, schemas
from app.crud.crud_base import CRUDBase

from app.core.security import verify_password

from sqlalchemy.orm import Session


class CRUDUsers(CRUDBase):
    def authenticate_user(self, user_login: schemas.UserLogin, db: Session) -> schemas.models.UserRoles:
        """ 
        Autentica que el usuario sí esté en la base de datos cuando se registre

        Args:
            user_login (schemas.UserLogin): Información de un usuario para entrar al sistema
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

        Returns:
            schemas.models.UserRoles | None: Retorna un objeto `schemas.models.UserRoles` si el usuario sí fue autenticado
            correctamente. En caso contrario retorna `None`.
        """
        user_search: schemas.UserSearch = schemas.UserSearch(num_document=user_login.num_document, rol=user_login.rol)
        user: models.UserRoles | None = self.get_user_rol(user_search, db)

        if user is None:
            return None
        if not verify_password(user_login.password, user.password):
            return None
        
        return schemas.models.UserRoles.model_validate(user)

    def get_users(self, db: Session, rol: bool = False, active: bool = True) -> list[schemas.UserBase] | list[schemas.UserAll]:
        """
        Obtiene todos los usuarios dentro del sistema.

        Args:
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql
            rol (bool): Se especifica si se muestra todos los roles del mismo usuario.
                Cuando `rol=True`, entonces la función retorna un objeto del tipo `list[UserAll]` y `list[UserInfo]` cuando `rol=False`.
                Por defecto `rol=False`.
            active (bool): Filtro de solo los usuarios que al menos tengan un rol activo dentro del hospital. Por defecto `active=True`.
        
        Returns:
            list[schemas.UserBase] | list[schemas.UserAll]: Cuando `rol=False`, la función list[schemas.UserBase], en caso de que
            `rol=True`, entonces se retorna `list[schema.UserAll]`
        """
        stmt = self.__join_users(active=active)
        query: list = db.execute(stmt).all()
        num_documents: set[str] = set(map(lambda row: row[0], query))
        result: list[schemas.UserBase | schemas.UserAll] = []

        for num_document in num_documents:
            data_num_document = list(filter(
                lambda row: row[0]==num_document, query)
            )
            userbase = self.__create_user_base(data_num_document[0])

            if rol:
                roles = list(map(lambda row: (row[-2], row[-1]), data_num_document))
                userall: schemas.UserAll = schemas.UserAll(
                    **userbase.model_dump(),
                    roles=roles
                )
                result.append(userall)
            else:
                result.append(userbase)

        return result

    def get_user(self, num_document: str, db: Session, rol: bool = False, active: bool = True) -> schemas.UserBase | schemas.UserAll | None:
        """
        Obtiene la información básica de un usuario del sistema sin importar el rol 
        
        Args:
            num_document (str): Número de documento del usuario que se desea encontrar.
            db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.
            rol (bool): Se especifica si se muestra todos los roles del mismo usuario.
                Cuando `rol=True`, entonces la función retorna un objeto del tipo `UserAll` y `UserInfo` cuando `rol=False`.
                Por defecto `rol=False`.
            active (bool): Filtro de que el usuario tenga al menos un rol activo dentro del hospital. Por defecto `active=True`.

        Returns:
            schemas.UserBase | schemas.UserAll: Cuando `rol=False` la función retorna `schemas.UserBase`, en caso de que
            `rol=True`, entonces se retorna `schema.UserAll`.

            En caso de no encontrar al usuario, retorna `None`.
        """
        stmt = self.__join_users(active).where(models.UsersInfo.num_document == num_document)
        query = db.execute(stmt).all()
        if not query:  # Si está vacía
            return None

        userbase = self.__create_user_base(query[0])
        if rol:
            roles = list(map(lambda row: (row[-2], row[-1]), query))
            return schemas.UserAll(**userbase.model_dump(), roles=roles)
        
        return userbase


crud_user: CRUDUsers = CRUDUsers()
