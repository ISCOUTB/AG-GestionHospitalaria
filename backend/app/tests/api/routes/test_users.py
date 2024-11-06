from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password

from app.tests.utils.utils import random_document
from app.tests.utils.utils import random_password
from app.tests.utils.user import create_random_user
from app.tests.utils.user import non_existent_document
from app.tests.utils.hospitalizations import create_random_hospitalization

from app import schemas

from app.crud import crud_admin

endpoint = f"{settings.API_V1_STR}/users"


def test_create_user(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    admin = schemas.UserCreate(
        num_document=random_document(), password=random_password(10), rol="admin"
    )

    response = client.post(
        f"{endpoint}/", headers=superuser_token, json=admin.model_dump()
    )

    assert response.status_code == 201

    content = response.json()
    assert content["detail"] == "Usuario creado"

    user_search = schemas.UserSearch(num_document=admin.num_document, rol="admin")

    admin_in = crud_admin.get_user_rol(user_search, db)

    assert admin.num_document == admin_in.num_document
    assert verify_password(admin.password, admin_in.password)
    assert admin.rol == admin_in.rol


def test_create_user_non_superuser(
    client: TestClient, non_superuser_token: dict[str, str]
) -> None:
    admin = schemas.UserCreate(
        num_document=random_document(), password=random_password(10), rol="admin"
    )

    response = client.post(
        f"{endpoint}/", headers=non_superuser_token, json=admin.model_dump()
    )

    assert response.status_code == 403


def test_create_user_user_found(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    admin_in = create_random_user("admin", db, 10)
    data = schemas.UserCreate(
        num_document=admin_in.num_document, password=random_password(10), rol="admin"
    )

    response = client.post(
        f"{endpoint}/", headers=superuser_token, json=data.model_dump()
    )

    assert response.status_code == 409


def test_update_user(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    admin = create_random_user("admin", db, 10)

    new_password = (random_password(15),)
    new_email = "new_email"
    new_document = f"{admin.num_document}new"
    updated_info = schemas.UserUpdateAll(
        password=new_password, email=new_email, num_document=new_document
    )

    response = client.put(
        f"{endpoint}/{admin.num_document}",
        headers=superuser_token,
        json=updated_info.model_dump(),
    )

    assert response.status_code == 200

    content = response.json()
    assert content["detail"] == "Información del usuario actualizada"

    user_search = schemas.UserSearch(num_document=admin.num_document, rol="admin")

    admin_rol = crud_admin.get_user_rol(user_search, db)
    admin_info = crud_admin.get_user_info(admin.num_document, db)

    assert verify_password(new_password, admin_rol.password)
    assert admin_info.email == new_email
    assert admin_info.num_document == new_document


def test_update_user_non_superuser(
    client: TestClient, non_superuser_token: dict[str, str], db: Session
) -> None:
    admin = create_random_user("admin", db, 10)
    empty_info = schemas.UserUpdateAll()

    response = client.put(
        f"{endpoint}/{admin.num_document}",
        headers=non_superuser_token,
        json=empty_info.model_dump(),
    )

    assert response.status_code == 403


def test_update_user_user_not_found(
    client: TestClient, superuser_token: dict[str, str]
) -> None:
    empty_info = schemas.UserUpdateAll()

    response = client.put(
        f"{endpoint}/{non_existent_document}",
        headers=superuser_token,
        json=empty_info.model_dump(),
    )

    assert response.status_code == 404


def test_update_user_num_document_used(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    admin_params = ("admin", db, 10)
    admin1 = create_random_user(*admin_params)
    admin2 = create_random_user(*admin_params)

    updated_info_admin1 = schemas.UserUpdateAll(num_document=admin2.num_document)

    response = client.put(
        f"{endpoint}/{admin1.num_document}",
        headers=superuser_token,
        json=updated_info_admin1.model_dump(),
    )

    assert response.status_code == 409


def test_delete_user(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    user = create_random_user("admin", db, 10)

    response = client.delete(
        f"{endpoint}/{user.num_document}/{user.rol}", headers=superuser_token
    )

    assert response.status_code == 200

    content = response.json()
    assert content["detail"] == "Usuario eliminado"

    user_search = schemas.UserSearch(num_document=user.num_document, rol=user.rol)
    user_in = crud_admin.get_user_rol(user_search, db, False)
    assert user_in.is_active == False


def test_delete_user_user_not_found(
    client: TestClient, superuser_token: dict[str, str]
) -> None:
    response = client.delete(
        f"{endpoint}/{non_existent_document}/admin", headers=superuser_token
    )

    assert response.status_code == 404


def test_delete_user_non_superuser(
    client: TestClient, non_superuser_token: dict[str, str], db: Session
) -> None:
    admin = create_random_user("admin", db, 10)

    response = client.delete(
        f"{endpoint}/{admin.num_document}/{admin.rol}", headers=non_superuser_token
    )

    assert response.status_code == 403


def test_delete_user_patient_in_bed(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    hospitalization = create_random_hospitalization(db)
    response = client.delete(
        f"{endpoint}/{hospitalization.num_doc_patient}/patient", headers=superuser_token
    )

    assert response.status_code == 409


def test_get_user(client: TestClient, superuser_token: dict[str, str], db: Session) -> None:
    user = create_random_user("admin", db, 10)

    response = client.get(
        f"{endpoint}/{user.num_document}?rol=true", headers=superuser_token
    )

    content = response.json()

    assert content["num_document"] == user.num_document
    assert ("admin", True) in content["roles"]


def test_get_user_user_not_found(
    client: TestClient, superuser_token: dict[str, str]
) -> None:
    response = client.get(f"{endpoint}/{non_existent_document}", headers=superuser_token)

    assert response.status_code == 404
