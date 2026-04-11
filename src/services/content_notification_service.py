from src.clients.discord_client import discord_client
from src.repositories.content_repository import content_repository
from src.repositories.notification_log_repository import notification_log_repository
from src.utils.datetime_utils import now_kst
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ContentNotificationService:
    def send_immediate_alerts(self) -> None:
        now_at = now_kst()
        targets = content_repository.find_immediate_targets()

        processed_count = 0

        for content in targets:
            notification_type = "content_immediate"

            already_sent = notification_log_repository.exists_success_log(
                target_type="content",
                target_id=content["id"],
                notification_type=notification_type,
            )

            if already_sent:
                continue

            message = self._build_message(content)

            try:
                discord_client.send_message(message)

                content_repository.mark_immediate_sent(
                    content_id=content["id"],
                    now_at=now_at,
                )

                notification_log_repository.create_log(
                    target_type="content",
                    target_id=content["id"],
                    notification_type=notification_type,
                    status="success",
                    sent_at=now_at,
                    message_preview=message[:200],
                )

                processed_count += 1

            except Exception:
                notification_log_repository.create_log(
                    target_type="content",
                    target_id=content["id"],
                    notification_type=notification_type,
                    status="failed",
                    sent_at=now_at,
                    message_preview=message[:200],
                )
                logger.exception("Failed to send content alert: content_id=%s", content["id"])

        logger.info("Content immediate alert completed: %s messages processed", processed_count)

    def _build_message(self, content) -> str:
        author = content["author_name"] or "-"
        published_at = content["published_at"] or "-"
        source_name = content["source_name"]

        return (
            "[새 기술 콘텐츠 알림]\n"
            f"- 출처: {source_name}\n"
            f"- 제목: {content['title']}\n"
            f"- 작성자: {author}\n"
            f"- 발행일: {published_at}\n"
            f"- 링크: {content['url']}"
        )


content_notification_service = ContentNotificationService()