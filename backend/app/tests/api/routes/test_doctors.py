from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.user import create_random_user
from app.tests.utils.user import non_existent_document
from app.tests.utils.doctor import create_doctor_info
from app.tests.utils.doctor import create_new_speciality
from app.tests.utils.doctor import create_random_speciality


from app.crud import crud_doctor

endpoint = f"{settings.API_V1_STR}/doctors"


def test_get_doctor(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    doctor = create_random_user("doctor", db, 10)

    response = client.get(f"{endpoint}/{doctor.num_document}", headers=admin_token)

    content = response.json()

    assert response.status_code == 200
    assert content["num_document"] == doctor.num_document


def test_get_doctor_doctor_not_found(
    client: TestClient, admin_token: dict[str, str]
) -> None:
    response = client.get(f"{endpoint}/{non_existent_document}", headers=admin_token)

    assert response.status_code == 404


def test_get_speciality_doctor(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    speciality = create_new_speciality(db)
    doctor1 = create_random_user("doctor", db, 10)
    doctor2 = create_random_user("doctor", db, 10)

    # Debería cumplirse siempre
    assert crud_doctor.add_doctor_speciality(doctor1.num_document, db, speciality) == 0
    assert crud_doctor.add_doctor_speciality(doctor2.num_document, db, speciality) == 0

    response = client.get(
        f"{endpoint}/specialities/{speciality.name}", headers=admin_token
    )

    content = response.json()

    assert response.status_code == 200
    for doctor in content:
        assert doctor["num_document"] in (doctor1.num_document, doctor2.num_document)
        assert doctor["specialities"][0]["name"] == speciality.name


def test_add_doctor_speciality(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    doctor = create_random_user("doctor", db, 10)
    speciality1 = create_new_speciality(db)
    speciality2 = create_random_speciality()

    response1 = client.post(
        f"{endpoint}/{doctor.num_document}",
        headers=admin_token,
        json={"name": speciality1.name, "description": None},
    )

    response2 = client.post(
        f"{endpoint}/{doctor.num_document}",
        headers=admin_token,
        json=speciality2.model_dump(),
    )

    i = 0
    for speciality, response in zip((speciality1, speciality2), (response1, response2)):
        assert response.status_code == 201

        content = response.json()
        assert content["detail"] == "Especialidad agregada al doctor"

        doctor_in = crud_doctor.get_doctor(doctor.num_document, db)

        assert doctor.num_document == doctor_in.num_document
        assert speciality.name == doctor_in.specialities[i].name

        i += 1


def test_add_doctor_speciality_doctor_not_found(
    client: TestClient, admin_token: dict[str, str]
) -> None:
    speciality = create_random_speciality()

    response = client.post(
        f"{endpoint}/{non_existent_document}",
        headers=admin_token,
        json=speciality.model_dump(),
    )

    assert response.status_code == 404


def test_add_doctor_speciality_speciality_not_found(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    doctor = create_random_user("doctor", db, 10)
    speciality = create_random_speciality()

    response = client.post(
        f"{endpoint}/{doctor.num_document}",
        headers=admin_token,
        json={"name": speciality.name, "description": None},
    )

    assert response.status_code == 400


def test_add_doctor_speciality_speciality_doctor_found(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    doctor = create_doctor_info(db)
    speciality = doctor.specialities[0]

    response = client.post(
        f"{endpoint}/{doctor.num_document}",
        headers=admin_token,
        json={"name": speciality.name, "description": None},
    )

    assert response.status_code == 409


def test_delete_speciality(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    doctor = create_doctor_info(db)
    speciality = doctor.specialities[0]

    response = client.delete(
        f"{endpoint}/{doctor.num_document}?speciality_name={speciality.name}",
        headers=admin_token,
    )

    assert response.status_code == 200

    content = response.json()
    assert content["detail"] == "Especialidad borrada del doctor"

    doctor_in = crud_doctor.get_doctor(doctor.num_document, db)
    assert doctor.num_document == doctor_in.num_document
    assert not doctor_in.specialities  # Lista vacía


def test_delete_speciality_doctor_not_found(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    speciality = create_new_speciality(db)

    response = client.delete(
        f"{endpoint}/{non_existent_document}?speciality_name={speciality.name}",
        headers=admin_token,
    )

    assert response.status_code == 404


def test_delete_speciality_speciality_not_found(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    doctor = create_doctor_info(db)
    speciality = create_random_speciality()

    response = client.delete(
        f"{endpoint}/{doctor.num_document}?speciality_name={speciality.name}",
        headers=admin_token,
    )

    assert response.status_code == 404


def test_delete_speciality_speciality_doctor_not_found(
    client: TestClient, admin_token: dict[str, str], db: Session
) -> None:
    doctor = create_random_user("doctor", db, 10)
    speciality = create_doctor_info(db).specialities[0]

    response = client.delete(
        f"{endpoint}/{doctor.num_document}?speciality_name={speciality.name}",
        headers=admin_token,
    )

    assert response.status_code == 409
