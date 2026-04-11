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


def days_until(start_at: datetime, now_at: datetime) -> int:
    if isinstance(start_at, str):
        start_at = datetime.fromisoformat(start_at)

    start_date = start_at.astimezone(KST).date()
    now_date = now_at.astimezone(KST).date()
    return (start_date - now_date).days


def get_calendar_notification_type(days_left: int) -> str | None:
    if days_left == 7:
        return "calendar_7d"
    if days_left == 3:
        return "calendar_3d"
    if days_left == 1:
        return "calendar_1d"
    return None


def parse_rss_published_datetime(entry) -> datetime | None:
    published_parsed = getattr(entry, "published_parsed", None)
    updated_parsed = getattr(entry, "updated_parsed", None)

    target = published_parsed or updated_parsed
    if target is None:
        return None

    return datetime(
        year=target.tm_year,
        month=target.tm_mon,
        day=target.tm_mday,
        hour=target.tm_hour,
        minute=target.tm_min,
        second=target.tm_sec,
        tzinfo=timezone.utc,
    ).astimezone(KST)


# 오늘 일정
def get_today_range():
    now = datetime.now()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end


# 이번주 일정
def get_this_week_range():
    now = datetime.now()
    start = now - timedelta(days=now.weekday())
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=7)
    return start, end


# 이번달 일정
def get_this_month_range():
    now = datetime.now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    if now.month == 12:
        end = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        end = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)

    return start, end