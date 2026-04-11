from src.clients.discord.webhook_client import discord_client
from src.utils.logger import get_logger

logger = get_logger(__name__)


class NotificationService:
    def send_test_message(self) -> None:
        message = "[테스트] GitHub Actions / 로컬 실행 확인 메시지입니다."
        discord_client.send_message(message)
        logger.info("Test notification flow completed")


notification_service = NotificationService()