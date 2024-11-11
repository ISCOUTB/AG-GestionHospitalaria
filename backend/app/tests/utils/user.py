from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import crud_admin
from app.schemas import UserCreate, UserSearch, Roles
from app.models import UserRoles
from app.core.config import settings
from app.tests.utils.utils import random_document, random_password


non_existent_document = "NonExistentDocument"


def fill_random_user(rol: Roles, k: int) -> UserCreate:
    num_document = random_document()
    password = random_password(k)

    new_user = UserCreate(num_document=num_document, rol=rol, password=password)

    return new_user


def create_random_user(rol: Roles, db: Session, k: int) -> UserRoles:
    new_user = fill_random_user(rol, k)

    # Validar que se cree un nuevo usuario
    out = crud_admin.create_user(new_user, db, True)
    while out == 2:
        new_user = fill_random_user(rol, k)
        out = crud_admin.create_user(new_user, db, True)

    user_search = UserSearch(num_document=new_user.num_document, rol=rol)
    return crud_admin.get_user_rol(user_search, db)


def get_non_superuser_token(client: TestClient, db: Session) -> dict[str, str]:
    new_user = UserCreate(
        num_document=random_document(),
        password=random_password(10),
        rol="admin",
    )

    assert crud_admin.create_user(new_user, db, True) == 0

    login_data = {
        "username": new_user.num_document,
        "password": new_user.password,
        "rol": new_user.rol,
    }

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def get_doctor_token(client: TestClient, db: Session) -> dict[str, str]:
    new_user = UserCreate(
        num_document=random_document(),
        password=random_password(10),
        rol="doctor",
    )

    assert crud_admin.create_user(new_user, db) == 0

    login_data = {
        "username": new_user.num_document,
        "password": new_user.password,
        "rol": new_user.rol,
    }

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
