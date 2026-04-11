from src.domains.content.service import content_service
from src.domains.content.alert_service import content_alert_service


def run():
    content_service.collect_recent_rss_contents(hours=24)
    content_alert_service.send_recent_contents_digest(hours=24)
    content_service.delete_old_contents(days=3)