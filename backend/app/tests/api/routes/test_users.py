import os

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


def test_create_patient_files(
    client: TestClient, non_superuser_token: dict[str, str], db: Session    
) -> None:
    patient = schemas.UserCreate(
        num_document=random_document(), password=random_password(10), rol="patient"
    )

    response = client.post(
        f"{endpoint}/", headers=non_superuser_token, json=patient.model_dump()
    )

    assert response.status_code == 201

    assert os.path.exists(
        os.path.join(settings.PATIENT_DOCS_PATH, patient.num_document)
    )
    assert os.path.exists(
        os.path.join(settings.PATIENT_DOCS_PATH, patient.num_document, settings.HISTORY_FILENAME)
    )
    assert os.path.exists(
        os.path.join(settings.PATIENT_DOCS_PATH, patient.num_document, "histories")
    )
    assert os.path.exists(
        os.path.join(settings.PATIENT_DOCS_PATH, patient.num_document, "orders")
    )
    assert os.path.exists(
        os.path.join(settings.PATIENT_DOCS_PATH, patient.num_document, "results")
    )


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

    assert admin_in is not None
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


def test_create_user_invalid_email_bad(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    data = schemas.UserCreate(
        num_document=random_document(),
        password=random_password(10),
        rol="admin",
        email="bad_email",
    )

    response = client.post(
        f"{endpoint}/", headers=superuser_token, json=data.model_dump()
    )

    assert response.status_code == 409


def test_create_user_invalid_email_repeated(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    # Agregar un usuario con este email
    num_document = random_document()
    email = f"{num_document}@email.com"
    data = schemas.UserCreate(
        num_document=num_document,
        password=random_password(10),
        rol="admin",
        email=email,
    )

    response = client.post(
        f"{endpoint}/", headers=superuser_token, json=data.model_dump()
    )

    assert response.status_code == 201

    # Crear nuevo usuario con este email para validar
    data = schemas.UserCreate(
        num_document=random_document(),
        password=random_password(10),
        rol="admin",
        email=email,
    )

    response = client.post(
        f"{endpoint}/", headers=superuser_token, json=data.model_dump()
    )

    assert response.status_code == 409


def test_update_user(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    admin = create_random_user("admin", db, 10)

    new_password = random_password(15)
    new_document = f"{admin.num_document}new"
    updated_info = schemas.UserUpdateAll(
        password=new_password, num_document=new_document
    )

    response = client.put(
        f"{endpoint}/{admin.num_document}/{admin.rol}",
        headers=superuser_token,
        json=updated_info.model_dump(),
    )

    assert response.status_code == 200

    content = response.json()
    assert content["detail"] == "Información del usuario actualizada"

    user_search = schemas.UserSearch(num_document=new_document, rol="admin")
    admin_rol = crud_admin.get_user_rol(user_search, db)
    admin_info = crud_admin.get_user_info(new_document, db)

    assert verify_password(new_password, str(admin_rol.password))
    assert admin_info.num_document == new_document


def test_update_patient_document(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    patient = schemas.UserCreate(
        num_document=random_document(), password=random_password(10), rol="patient"
    )

    response = client.post(
        f"{endpoint}/", headers=superuser_token, json=patient.model_dump()
    )

    assert response.status_code == 201

    new_document = f"{patient.num_document}new"
    updated_info = schemas.UserUpdateAll(
        num_document=new_document
    )

    response = client.put(
        f"{endpoint}/{patient.num_document}/{patient.rol}",
        headers=superuser_token,
        json=updated_info.model_dump(),
    )

    assert response.status_code == 200
    assert not os.path.exists(
        os.path.join(settings.PATIENT_DOCS_PATH, str(patient.num_document))
    )
    assert os.path.exists(
        os.path.join(settings.PATIENT_DOCS_PATH, new_document)
    )


def test_update_user_non_superuser(
    client: TestClient, non_superuser_token: dict[str, str], db: Session
) -> None:
    admin = create_random_user("admin", db, 10)
    empty_info = schemas.UserUpdateAll()

    response = client.put(
        f"{endpoint}/{admin.num_document}/{admin.rol}",
        headers=non_superuser_token,
        json=empty_info.model_dump(),
    )

    assert response.status_code == 403


def test_update_user_user_not_found(
    client: TestClient, superuser_token: dict[str, str]
) -> None:
    empty_info = schemas.UserUpdateAll()

    response = client.put(
        f"{endpoint}/{non_existent_document}/doctor",
        headers=superuser_token,
        json=empty_info.model_dump(),
    )

    assert response.status_code == 404


def test_update_user_num_document_used(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    params = ("admin", db, 10)
    admin1 = create_random_user(*params)
    admin2 = create_random_user(*params)

    updated_info_admin1 = schemas.UserUpdateAll(num_document=admin2.num_document)

    response = client.put(
        f"{endpoint}/{admin1.num_document}/{params[0]}",
        headers=superuser_token,
        json=updated_info_admin1.model_dump(),
    )

    assert response.status_code == 409


def test_update_user_invalid_email_bad(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    user = create_random_user("admin", db, 10)
    data = schemas.UserUpdateAll(email="bad_email")

    response = client.put(
        f"{endpoint}/{user.num_document}/{user.rol}",
        headers=superuser_token,
        json=data.model_dump(),
    )

    assert response.status_code == 409


def test_update_user_invalid_email_repeated(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    user1 = create_random_user("admin", db, 10)
    email = f"{user1.num_document}@test.com"
    data = schemas.UserUpdateAll(email=email)

    response = client.put(
        f"{endpoint}/{user1.num_document}/{user1.rol}",
        headers=superuser_token,
        json=data.model_dump(),
    )

    assert response.status_code == 200

    user = create_random_user("admin", db, 10)
    response = client.put(
        f"{endpoint}/{user.num_document}/{user.rol}",
        headers=superuser_token,
        json=data.model_dump(),
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
    user_in = crud_admin.get_user_rol(user_search, db)
    assert user_in is None


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


def test_get_user(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    user = create_random_user("admin", db, 10)

    response = client.get(
        f"{endpoint}/{user.num_document}?rol=true", headers=superuser_token
    )

    content = response.json()

    assert content["num_document"] == user.num_document
    assert ["admin", True] in content["roles"]


def test_get_user_user_not_found(
    client: TestClient, superuser_token: dict[str, str]
) -> None:
    response = client.get(
        f"{endpoint}/{non_existent_document}", headers=superuser_token
    )

    assert response.status_code == 404
