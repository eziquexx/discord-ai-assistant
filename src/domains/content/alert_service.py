from datetime import timedelta

from src.clients.discord.webhook_client import discord_client
from src.domains.content.repository import content_repository
from src.domains.notification.repository import notification_log_repository
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

    def send_recent_contents_digest(self, hours: int = 24) -> None:
        now_at = now_kst()
        window_start = now_at - timedelta(hours=hours)

        contents = content_repository.find_contents_between(window_start, now_at)

        if not contents:
            logger.info(
                "No recent RSS contents found (window_start=%s, window_end=%s)",
                window_start,
                now_at,
            )
            return

        messages = self._build_digest_messages(contents, window_start, now_at)

        for message in messages:
            discord_client.send_message(message)

        logger.info(
            "Recent RSS digest sent: %s contents, %s messages",
            len(contents),
            len(messages),
        )


    def _build_digest_messages(
        self,
        contents: list[dict],
        window_start,
        window_end,
        max_length: int = 1900,
    ) -> list[str]:
        header = (
            "[새로 올라온 글]\n"
            f"- 조회 범위: {window_start.strftime('%Y-%m-%d %H:%M')} ~ {window_end.strftime('%Y-%m-%d %H:%M')}\n\n"
            "[글 목록]\n"
        )

        messages = []
        current_message = header

        for content in contents:
            line = self._build_digest_line(content)

            if len(current_message) + len(line) > max_length:
                messages.append(current_message.rstrip())
                current_message = header + line
            else:
                current_message += line

        if current_message.strip():
            messages.append(current_message.rstrip())

        return messages


    def _build_digest_line(self, content: dict) -> str:
        published_at = content["published_at"]

        if hasattr(published_at, "strftime"):
            date_text = published_at.strftime("%Y-%m-%d %H:%M")
        else:
            date_text = str(published_at).replace("T", " ")[:16]

        title = content["title"]
        source_name = content["source_name"]
        url = content["url"]

        return (
            f"- [{date_text}] {title}\n"
            f"  {source_name}\n"
            f"  링크 --> <{url}>\n"
        )


content_alert_service = ContentNotificationService()