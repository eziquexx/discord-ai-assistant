from src.db.init_db import (
    initialize_database,
    clear_notification_logs,
    reset_calendar_notification_flags,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DBService:
    def initialize(self) -> None:
        initialize_database()
        logger.info("DB init flow completed")


    # 테스트용 데이터 초기화 함수들, 실제 운영에서는 쓰지 말 것
    def reset_test_data(self) -> None:
        clear_notification_logs()
        reset_calendar_notification_flags()
        logger.info("DB test data reset completed")


db_service = DBService()