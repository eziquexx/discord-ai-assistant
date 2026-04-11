from datetime import datetime
import sqlite3

from src.repositories.base_repository import BaseRepository


class ContentRepository(BaseRepository):
    def exists_by_source_id(self, source_name: str, source_id: str) -> bool:
        if not source_id:
            return False

        connection = self.get_connection()

        try:
            row = connection.execute(
                """
                SELECT id
                FROM contents
                WHERE source_name = ?
                  AND source_id = ?
                LIMIT 1
                """,
                (source_name, source_id),
            ).fetchone()

            return row is not None
        finally:
            connection.close()

    def exists_by_url(self, url: str) -> bool:
        connection = self.get_connection()

        try:
            row = connection.execute(
                """
                SELECT id
                FROM contents
                WHERE url = ?
                LIMIT 1
                """,
                (url,),
            ).fetchone()

            return row is not None
        finally:
            connection.close()

    def exists_by_title_and_published_at(
        self,
        title: str,
        published_at: datetime | None,
    ) -> bool:
        if published_at is None:
            return False

        connection = self.get_connection()

        try:
            row = connection.execute(
                """
                SELECT id
                FROM contents
                WHERE title = ?
                  AND published_at = ?
                LIMIT 1
                """,
                (title, published_at.isoformat()),
            ).fetchone()

            return row is not None
        finally:
            connection.close()

    def create_content(
        self,
        source_type: str,
        source_name: str,
        source_id: str | None,
        title: str,
        url: str,
        author_name: str | None,
        published_at: datetime | None,
        collected_at: datetime,
        raw_text: str | None,
        summary: str | None,
        keywords: str | None,
        is_immediate_target: bool,
        is_briefing_target: bool,
        delete_after: datetime,
    ) -> None:
        connection = self.get_connection()

        try:
            connection.execute(
                """
                INSERT INTO contents (
                    source_type,
                    source_name,
                    source_id,
                    title,
                    url,
                    author_name,
                    published_at,
                    collected_at,
                    raw_text,
                    summary,
                    keywords,
                    is_immediate_target,
                    is_briefing_target,
                    immediate_sent,
                    briefing_sent,
                    created_at,
                    updated_at,
                    delete_after
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, ?, ?, ?)
                """,
                (
                    source_type,
                    source_name,
                    source_id,
                    title,
                    url,
                    author_name,
                    published_at.isoformat() if published_at else None,
                    collected_at.isoformat(),
                    raw_text,
                    summary,
                    keywords,
                    int(is_immediate_target),
                    int(is_briefing_target),
                    collected_at.isoformat(),
                    collected_at.isoformat(),
                    delete_after.isoformat(),
                ),
            )
            connection.commit()
        finally:
            connection.close()

    def find_immediate_targets(self):
        connection = self.get_connection()

        try:
            rows = connection.execute(
                """
                SELECT *
                FROM contents
                WHERE is_immediate_target = 1
                  AND immediate_sent = 0
                ORDER BY collected_at ASC
                """
            ).fetchall()

            return [dict(row) for row in rows]
        finally:
            connection.close()

    def mark_immediate_sent(self, content_id: int, now_at: datetime) -> None:
        connection = self.get_connection()

        try:
            connection.execute(
                """
                UPDATE contents
                SET immediate_sent = 1,
                    updated_at = ?
                WHERE id = ?
                """,
                (now_at.isoformat(), content_id),
            )
            connection.commit()
        finally:
            connection.close()

    def find_contents_between(self, start_at: datetime, end_at: datetime) -> list[dict]:
        connection = self.get_connection()
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    id,
                    source_name,
                    title,
                    url,
                    published_at,
                    collected_at
                FROM contents
                WHERE published_at >= ?
                  AND published_at < ?
                ORDER BY published_at DESC
                """,
                (start_at, end_at),
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            connection.close()

    def delete_contents_older_than(self, cutoff_at: datetime) -> int:
        connection = self.get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                DELETE FROM contents
                WHERE collected_at < ?
                """,
                (cutoff_at,),
            )
            deleted_count = cursor.rowcount
            connection.commit()
            return deleted_count
        finally:
            connection.close()

content_repository = ContentRepository()