from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.db import engine
from app.initial_data import init_db
from app.main import app

from app.tests.utils.utils import get_superuser_token
from app.tests.utils.user import get_doctor_token, get_non_superuser_token
from app.tests.utils.patient import get_patient_token


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def superuser_token(client: TestClient) -> dict[str, str]:
    return get_superuser_token(client)


@pytest.fixture(scope="module")
def non_superuser_token(client: TestClient, db: Session) -> dict[str, str]:
    return get_non_superuser_token(client, db)


@pytest.fixture(scope="module")
def nonpatient_token(client: TestClient) -> dict[str, str]:
    return get_superuser_token(client)


@pytest.fixture(scope="module")
def doctor_token(client: TestClient, db: Session) -> dict[str, str]:
    return get_doctor_token(client, db)


@pytest.fixture(scope="module")
def patient_token(client: TestClient, db: Session) -> dict[str, str]:
    return get_patient_token(client, db)
