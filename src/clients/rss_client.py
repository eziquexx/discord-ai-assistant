import feedparser

from src.utils.logger import get_logger

logger = get_logger(__name__)


class RSSClient:
    def fetch_feed(self, feed_url: str):
        feed = feedparser.parse(feed_url)

        if feed.bozo:
            logger.warning("RSS parse warning: %s", feed_url)

        entries = feed.entries or []
        logger.info("Fetched %s RSS entries from %s", len(entries), feed_url)
        return entries


rss_client = RSSClient()