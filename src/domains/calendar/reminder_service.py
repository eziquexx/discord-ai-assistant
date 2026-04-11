from src.clients.discord.webhook_client import discord_client
from src.domains.calendar.repository import calendar_event_repository
from src.domains.notification.repository import notification_log_repository
from src.utils.datetime_utils import (
    days_until,
    get_calendar_notification_type,
    now_kst,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CalendarReminderService:
    def send_reminders(self) -> None:
        now_at = now_kst()
        events = calendar_event_repository.find_reminder_targets(now_at)

        processed_count = 0

        for event in events:
            days_left = days_until(event["start_at"], now_at)
            notification_type = get_calendar_notification_type(days_left)

            if notification_type is None:
                continue

            if notification_type == "calendar_7d" and event["notified_7d"]:
                continue

            if notification_type == "calendar_3d" and event["notified_3d"]:
                continue

            if notification_type == "calendar_1d" and event["notified_1d"]:
                continue

            already_sent = notification_log_repository.exists_success_log(
                target_type="calendar_event",
                target_id=event["id"],
                notification_type=notification_type,
            )

            if already_sent:
                continue

            message = self._build_message(event, days_left)

            try:
                discord_client.send_message(message)

                calendar_event_repository.mark_notified(
                    event_id=event["id"],
                    notification_type=notification_type,
                    now_at=now_at,
                )

                notification_log_repository.create_log(
                    target_type="calendar_event",
                    target_id=event["id"],
                    notification_type=notification_type,
                    status="success",
                    sent_at=now_at,
                    message_preview=message[:200],
                )

                processed_count += 1

            except Exception:
                notification_log_repository.create_log(
                    target_type="calendar_event",
                    target_id=event["id"],
                    notification_type=notification_type,
                    status="failed",
                    sent_at=now_at,
                    message_preview=message[:200],
                )
                logger.exception("Failed to send calendar reminder: event_id=%s", event["id"])

        logger.info("Calendar reminder job completed: %s messages processed", processed_count)

    def _build_message(self, event, days_left: int) -> str:
        title = event["title"]
        location = event["location"] or "-"
        start_at = event["start_at"]

        return (
            "[일정 알림]\n"
            f"{days_left}일 후 일정이 있어요.\n\n"
            f"- 제목: {title}\n"
            f"- 시작: {start_at}\n"
            f"- 장소: {location}"
        )


calendar_reminder_service = CalendarReminderService()