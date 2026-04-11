from datetime import datetime
from src.utils.datetime_utils import parse_google_datetime

from src.repositories.base_repository import BaseRepository


class CalendarEventRepository(BaseRepository):
    def find_by_external_event_id(self, external_event_id: str):
        connection = self.get_connection()

        try:
            cursor = connection.execute(
                """
                SELECT *
                FROM calendar_events
                WHERE external_event_id = ?
                """,
                (external_event_id,),
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def upsert_event(
        self,
        external_event_id: str,
        title: str,
        description: str | None,
        location: str | None,
        start_at: datetime,
        end_at: datetime,
        is_all_day: bool,
        now_at: datetime,
        delete_after: datetime,
    ) -> None:
        connection = self.get_connection()

        try:
            existing = connection.execute(
                """
                SELECT id
                FROM calendar_events
                WHERE external_event_id = ?
                """,
                (external_event_id,),
            ).fetchone()

            if existing:
                connection.execute(
                    """
                    UPDATE calendar_events
                    SET title = ?,
                        description = ?,
                        location = ?,
                        start_at = ?,
                        end_at = ?,
                        is_all_day = ?,
                        updated_at = ?,
                        delete_after = ?
                    WHERE external_event_id = ?
                    """,
                    (
                        title,
                        description,
                        location,
                        start_at.isoformat(),
                        end_at.isoformat(),
                        int(is_all_day),
                        now_at.isoformat(),
                        delete_after.isoformat(),
                        external_event_id,
                    ),
                )
            else:
                connection.execute(
                    """
                    INSERT INTO calendar_events (
                        external_event_id,
                        title,
                        description,
                        location,
                        start_at,
                        end_at,
                        is_all_day,
                        notified_7d,
                        notified_3d,
                        notified_1d,
                        created_at,
                        updated_at,
                        delete_after
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 0, ?, ?, ?)
                    """,
                    (
                        external_event_id,
                        title,
                        description,
                        location,
                        start_at.isoformat(),
                        end_at.isoformat(),
                        int(is_all_day),
                        now_at.isoformat(),
                        now_at.isoformat(),
                        delete_after.isoformat(),
                    ),
                )

            connection.commit()
        finally:
            connection.close()



    def find_reminder_targets(self, now_at: datetime):
        connection = self.get_connection()

        try:
            cursor = connection.execute(
                """
                SELECT *
                FROM calendar_events
                WHERE end_at >= ?
                ORDER BY start_at ASC
                """,
                (now_at.isoformat(),),
            )
            return cursor.fetchall()
        finally:
            connection.close()


    def mark_notified(self, event_id: int, notification_type: str, now_at: datetime) -> None:
        connection = self.get_connection()

        try:
            if notification_type == "calendar_7d":
                connection.execute(
                  """
                  UPDATE calendar_events
                  SET notified_7d = 1,
                      updated_at = ?
                  WHERE id = ?
                  """,
                  (now_at.isoformat(), event_id),
                )
            elif notification_type == "calendar_3d":
                  connection.execute(
                      """
                      UPDATE calendar_events
                      SET notified_3d = 1,
                          updated_at = ?
                      WHERE id = ?
                      """,
                      (now_at.isoformat(), event_id),
                  )

            elif notification_type == "calendar_1d":
                connection.execute(
                    """
                    UPDATE calendar_events
                    SET notified_1d = 1,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (now_at.isoformat(), event_id),
                )

            connection.commit()
        finally:
            connection.close()


calendar_event_repository = CalendarEventRepository()