from src.domains.notification.service import notification_service

def run():
    notification_service.send_test_message()