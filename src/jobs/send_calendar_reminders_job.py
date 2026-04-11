from src.domains.calendar.reminder_service import calendar_reminder_service

def run():
    calendar_reminder_service.send_reminders()