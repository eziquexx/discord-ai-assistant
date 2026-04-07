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


# 테스트용 데이터 초기화 함수들, 실제 운영에서는 쓰지 말 것
def clear_notification_logs() -> None:
    connection = get_connection()

    try:
        connection.execute("DELETE FROM notification_logs")
        connection.commit()
        logger.info("Notification logs cleared successfully")
    finally:
        connection.close()


# 테스트용 데이터 초기화 함수들, 실제 운영에서는 쓰지 말 것
def reset_calendar_notification_flags() -> None:
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE calendar_events
            SET notified_7d = 0,
                notified_3d = 0,
                notified_1d = 0
            """
        )
        connection.commit()
        logger.info("Calendar notification flags reset successfully")
    finally:
        connection.close()