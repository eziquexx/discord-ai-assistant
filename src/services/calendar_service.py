from datetime import timedelta

from src.clients.google_calendar_client import google_calendar_client
from src.repositories.calendar_event_repository import calendar_event_repository
from src.utils.datetime_utils import (
    calculate_delete_after,
    now_kst,
    parse_google_date,
    parse_google_datetime,
    to_isoformat_utc,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CalendarService:
    def sync_events(self) -> None:
        now_at = now_kst()

        # 우선 MVP에서는 오늘부터 30일 뒤까지 조회
        time_min = to_isoformat_utc(now_at)
        time_max = to_isoformat_utc(now_at + timedelta(days=30))

        events = google_calendar_client.fetch_upcoming_events(
            time_min=time_min,
            time_max=time_max,
        )

        for event in events:
            external_event_id = event["id"]
            title = event.get("summary", "(제목 없음)")
            description = event.get("description")
            location = event.get("location")

            start_info = event.get("start", {})
            end_info = event.get("end", {})

            if "dateTime" in start_info:
                start_at = parse_google_datetime(start_info["dateTime"])
                end_at = parse_google_datetime(end_info["dateTime"])
                is_all_day = False
            else:
                start_at = parse_google_date(start_info["date"])
                end_at = parse_google_date(end_info["date"])
                is_all_day = True

            delete_after = calculate_delete_after(end_at)

            calendar_event_repository.upsert_event(
                external_event_id=external_event_id,
                title=title,
                description=description,
                location=location,
                start_at=start_at,
                end_at=end_at,
                is_all_day=is_all_day,
                now_at=now_at,
                delete_after=delete_after,
            )

        logger.info("Calendar sync completed: %s events processed", len(events))


calendar_service = CalendarService()