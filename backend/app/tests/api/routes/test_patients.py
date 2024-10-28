from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.user import create_random_user
from app.tests.utils.user import non_existent_document
from app.tests.utils.patient import create_random_patient
from app.tests.utils.patient import create_random_responsable

endpoint = f'{settings.API_V1_STR}/patients'


def test_get_patient(client: TestClient, nonpatient_token: dict[str, str], db: Session) -> None:
    pass
