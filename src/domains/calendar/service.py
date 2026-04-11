from datetime import datetime, timedelta

from src.clients.google.calendar_client import google_calendar_client
from src.domains.calendar.repository import calendar_event_repository
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
        
    
    # 조회 일정 목록
    def get_events_by_range(self, start_dt: datetime, end_dt: datetime) -> list:
        time_min = to_isoformat_utc(start_dt)
        time_max = to_isoformat_utc(end_dt)

        events = google_calendar_client.fetch_upcoming_events(
            time_min=time_min,
            time_max=time_max,
        )
        return events

# 조회 일정 메시지 포맷팅
def format_events_message(title: str, events: list) -> str:
    if not events:
        return f"[{title}]\n등록된 일정이 없습니다."

    lines = [f"[{title}]"]
    for event in events:
        start_info = event.get("start", {})

        # 시간 있는 일정
        if "dateTime" in start_info:
            dt = start_info["dateTime"]
            # 2026-04-09T22:30 → 2026-04-09 22:30
            event_time = dt[:16].replace("T", " ")

        # 종일 일정
        else:
            event_time = start_info.get("date", "")

        event_title = event.get("summary", "(제목 없음)")

        lines.append(f"- {event_time} {event_title}")

    return "\n".join(lines)

calendar_service = CalendarService()