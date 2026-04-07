from src.db.connection import get_connection
from src.db.schema import SCHEMA_SQL
from src.utils.logger import get_logger

logger = get_logger(__name__)


def initialize_database() -> None:
    connection = get_connection()

    try:
        connection.executescript(SCHEMA_SQL)
        connection.commit()
        logger.info("Database initialized successfully")
    finally:
        connection.close()