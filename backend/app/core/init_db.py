from app import schemas

from app.crud import crud_user, crud_admin

from app.core.config import settings
from app.core.db import SessionLocal

from sqlalchemy.orm import Session


def init_db(db: Session) -> None:
    superuser_search = schemas.UserSearch(
        num_document=settings.FIRST_SUPERUSER, rol="admin"
    )
    user_db = crud_user.get_user_rol(superuser_search, db)

    if user_db is None:
        create_super_user = schemas.UserCreate(
            num_document=settings.FIRST_SUPERUSER,
            rol="admin",
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )

        crud_admin.create_user(create_super_user, db, True)


if __name__ == "__main__":
    init_db(SessionLocal())
