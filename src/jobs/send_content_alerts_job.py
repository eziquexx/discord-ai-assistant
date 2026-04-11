from src.domains.content.alert_service import content_alert_service

def run():
    content_alert_service.send_immediate_alerts()