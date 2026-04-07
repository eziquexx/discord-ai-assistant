from src.db.init_db import initialize_database
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DBService:
    def initialize(self) -> None:
        initialize_database()
        logger.info("DB init flow completed")


db_service = DBService()