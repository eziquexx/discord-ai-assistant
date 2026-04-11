from src.domains.content.service import content_service

def run():
    content_service.collect_rss_contents()