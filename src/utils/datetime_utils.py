from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))

def now_kst() -> datetime:
    return datetime.now(KST)


def to_isoformat_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def calculate_delete_after(end_at: datetime) -> datetime:
    return end_at + timedelta(days=3)


def parse_google_datetime(value: str) -> datetime:
    # Google Calendar 응답은 보통 Z 또는 +09:00 형태로 온다.
    # fromisoformat 사용을 위해 Z를 +00:00으로 바꿔준다.
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_google_date(value: str) -> datetime:
    # 하루 종일 일정은 date 형식(YYYY-MM-DD)으로 온다.
    return datetime.fromisoformat(value + "T00:00:00+09:00")