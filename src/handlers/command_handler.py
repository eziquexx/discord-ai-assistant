from src.services.calendar_service import CalendarService, format_events_message
from src.utils.datetime_utils import get_today_range, get_this_week_range, get_this_month_range

calendar_service = CalendarService()

async def handle_command(message):
    content = message.content.strip()

    if content == "!오늘일정":
        start, end = get_today_range()
        events = calendar_service.get_events_by_range(start, end)
        response = format_events_message("오늘 일정", events)
        await message.channel.send(response)

    elif content == "!이번주일정":
        start, end = get_this_week_range()
        events = calendar_service.get_events_by_range(start, end)
        response = format_events_message("이번 주 일정", events)
        await message.channel.send(response)

    elif content == "!이번달일정":
        start, end = get_this_month_range()
        events = calendar_service.get_events_by_range(start, end)
        response = format_events_message("이번 달 일정", events)
        await message.channel.send(response)