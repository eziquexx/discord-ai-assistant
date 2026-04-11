from src.domains.calendar.service import calendar_service

def run():
    calendar_service.sync_events()