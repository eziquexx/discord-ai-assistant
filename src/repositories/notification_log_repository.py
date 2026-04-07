from datetime import datetime, timedelta

from src.repositories.base_repository import BaseRepository


class NotificationLogRepository(BaseRepository):
    def exists_success_log(
        self,
        target_type: str,
        target_id: int,
        notification_type: str,
    ) -> bool:
        connection = self.get_connection()
        
        try:
            row = connection.execute(
                """
                SELECT id
                FROM notification_logs
                WHERE target_type = ?
                  AND target_id = ?
                  AND notification_type = ?
                  AND status = 'success'
                LIMIT 1
                """,
                (target_type, target_id, notification_type),
            ).fetchone()

            return row is not None
        finally:
            connection.close()

    def create_log(
        self,
        target_type: str,
        target_id: int,
        notification_type: str,
        status: str,
        sent_at: datetime,
        message_preview: str | None,
        discord_channel: str | None = None,
    ) -> None:
        connection = self.get_connection()

        try:
            delete_after = sent_at + timedelta(days=7)

            connection.execute(
                """
                INSERT INTO notification_logs (
                    target_type,
                    target_id,
                    notification_type,
                    discord_channel,
                    sent_at,
                    status,
                    message_preview,
                    created_at,
                    delete_after
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    target_type,
                    target_id,
                    notification_type,
                    discord_channel,
                    sent_at.isoformat(),
                    status,
                    message_preview,
                    sent_at.isoformat(),
                    delete_after.isoformat(),
                ),
            )
            connection.commit()
        finally:
            connection.close()

notification_log_repository = NotificationLogRepository()