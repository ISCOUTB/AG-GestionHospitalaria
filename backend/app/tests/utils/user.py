from sqlalchemy.orm import Session

from app.crud import crud_admin

from app.schemas import UserCreate, UserSearch, Roles
from app.models import UserRoles
from app.tests.utils.utils import random_document, random_password


def create_random_user(rol: Roles, db: Session, k: int) -> UserRoles:
    num_document = random_document()
    password = random_password(k)
    
    new_user = UserCreate(
        num_document=num_document,
        rol=rol,
        password=password
    )

    # Validar que se cree un nuevo usuario
    out = crud_admin.create_user(new_user, db, True)
    while out == 2:
        out = crud_admin.create_user(new_user, db, True)

    user_search = UserSearch(num_document=num_document, rol=rol)
    return crud_admin.get_user_rol(user_search, db)
