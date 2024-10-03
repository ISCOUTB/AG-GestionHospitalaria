import logging

from sqlalchemy.orm import Session

from app.core.init_db import init_db
from app.core.db import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    session: Session = SessionLocal()
    try:
        init_db(session)
    finally:
        session.close()

    
def main() -> None:
    logger.info("Creando la información inicial")
    init()
    logger.info("Información inicial creada")


if __name__ == '__main__':
    main()
