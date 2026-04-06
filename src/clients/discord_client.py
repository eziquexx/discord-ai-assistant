# Discord Webhook 호출

import httpx

from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DiscordClient:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_message(self, content: str) -> None:
        payload = {
          "content": content
        }

        # timeout을 주지 않으면 네트워크 문제 때 오래 멈출 수 있다.
        with httpx.Client(timeout=10.0) as client:
            response = client.post(self.webhook_url, json=payload)

        if response.status_code >= 400:
            logger.error("Discord webhook request failed: %s", response.text)
            raise RuntimeError(
              f"Discord webhookrequest failed with status {response.status_code}"
            )

        logger.info("Discord message sent successfully")

discord_client = DiscordClient(settings.discord_webhook_url)