from collections import defaultdict

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

        grouped_events = defaultdict(list)
        success_targets = []

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

            grouped_events[days_left].append(event)
            success_targets.append((event["id"], notification_type, event))

        if not grouped_events:
            logger.info("Calendar reminder job completed: no reminder targets")
            return

        messages = self._build_grouped_messages(grouped_events)

        try:
            for message in messages:
                discord_client.send_message(message)

            for event_id, notification_type, event in success_targets:
                calendar_event_repository.mark_notified(
                    event_id=event_id,
                    notification_type=notification_type,
                    now_at=now_at,
                )

                preview_message = f"{event['title']} / {event['start_at']}"

                notification_log_repository.create_log(
                    target_type="calendar_event",
                    target_id=event_id,
                    notification_type=notification_type,
                    status="success",
                    sent_at=now_at,
                    message_preview=preview_message[:200],
                )

            logger.info(
                "Calendar reminder job completed: %s events processed, %s messages sent",
                len(success_targets),
                len(messages),
            )

        except Exception:
            logger.exception("Failed to send grouped calendar reminders")

            for event_id, notification_type, event in success_targets:
                preview_message = f"{event['title']} / {event['start_at']}"

                notification_log_repository.create_log(
                    target_type="calendar_event",
                    target_id=event_id,
                    notification_type=notification_type,
                    status="failed",
                    sent_at=now_at,
                    message_preview=preview_message[:200],
                )

    def _build_grouped_messages(self, grouped_events: dict[int, list[dict]], max_length: int = 1900) -> list[str]:
        header = ".\n\n📌 일정 알림\n\n"
        footer = "\n\n----------------"

        section_order = [1, 3, 7]

        messages = []
        current_message = header

        for days_left in section_order:
            events = grouped_events.get(days_left, [])
            if not events:
                continue

            section = [f"[{days_left}일 후]"]

            for event in events:
                title = event["title"]
                location = event["location"] or "-"
                start_at_text = self._format_datetime(event["start_at"])

                section.append(f"- {title} / {start_at_text} / {location}")

            section_text = "\n".join(section) + "\n\n"

            if len(current_message) + len(section_text) > max_length:
                messages.append(current_message.rstrip() + footer)
                current_message = header + section_text
            else:
                current_message += section_text

        if current_message.strip():
            messages.append(current_message.rstrip() + footer)

        return messages

    def _format_datetime(self, value) -> str:
        if hasattr(value, "strftime"):
            return value.strftime("%Y-%m-%d %H:%M")
        return str(value).replace("T", " ")[:16]


calendar_reminder_service = CalendarReminderService()