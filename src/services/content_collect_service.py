from datetime import timedelta
from urllib.parse import urlparse

from src.clients.rss_client import rss_client
from src.config.settings import settings
from src.repositories.content_repository import content_repository
from src.utils.datetime_utils import now_kst, parse_rss_published_datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ContentCollectService:
    def collect_rss_contents(self) -> None:
        now_at = now_kst()
        feed_urls = self._get_feed_urls()

        inserted_count = 0

        for feed_url in feed_urls:
            source_name = self._build_source_name(feed_url)
            entries = rss_client.fetch_feed(feed_url)

            for entry in entries:
                source_id = getattr(entry, "id", None)
                title = getattr(entry, "title", "(제목 없음)")
                url = getattr(entry, "link", None)
                author_name = getattr(entry, "author", None)
                published_at = parse_rss_published_datetime(entry)

                if not url:
                    continue

                if source_id and content_repository.exists_by_source_id(source_name, source_id):
                    continue

                if content_repository.exists_by_url(url):
                    continue

                if content_repository.exists_by_title_and_published_at(title, published_at):
                    continue

                content_repository.create_content(
                    source_type="rss",
                    source_name=source_name,
                    source_id=source_id,
                    title=title,
                    url=url,
                    author_name=author_name,
                    published_at=published_at,
                    collected_at=now_at,
                    raw_text=None,
                    summary=None,
                    keywords=None,
                    is_immediate_target=True,
                    is_briefing_target=True,
                    delete_after=now_at + timedelta(days=14),
                )
                inserted_count += 1

        logger.info("RSS collect completed: %s contents inserted", inserted_count)

    def _get_feed_urls(self) -> list[str]:
        if not settings.rss_feed_urls.strip():
            return []

        return [
            item.strip()
            for item in settings.rss_feed_urls.split(",")
            if item.strip()
        ]

    def _build_source_name(self, feed_url: str) -> str:
        parsed = urlparse(feed_url)
        host = parsed.netloc.replace("www.", "").replace(".", "_")
        path = parsed.path.strip("/").replace("/", "_")

        if path:
            return f"{host}_{path}"
        return host


content_collect_service = ContentCollectService()