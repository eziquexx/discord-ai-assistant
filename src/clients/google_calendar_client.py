from google.oauth2 import service_account
from googleapiclient.discovery import build

from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GoogleCalendarClient:
    def __init__(self) -> None:
        self.scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

    def _build_service(self):
        if settings.google_service_account_json:
            info = json.loads(settings.google_service_account_json)

            credentials = service_account.Credentials.from_service_account_info(
              info,
              scopes=self.scopes,
            )
        else:
            credentials = service_account.Credentials.from_service_account_file(
              settings.google_service_account_file,
              scopes=self.scopes,
            )

        return build("calendar", "v3", credentials=credentials)

    def fetch_upcoming_events(self, time_min: str, time_max: str) -> list[dict]:
        service = self._build_service()

        response = (
            service.events()
            .list(
                calendarId=settings.google_calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        items = response.get("items", [])
        logger.info("Fetched %s calendar events", len(items))
        return items


google_calendar_client = GoogleCalendarClient()