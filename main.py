import argparse

from src.services.notification_service import notification_service
from src.utils.logger import get_logger
from src.services.db_service import db_service
from src.services.calendar_service import calendar_service
from src.services.calendar_reminder_service import calendar_reminder_service
from src.services.content_collect_service import content_collect_service
from src.services.content_notification_service import content_notification_service

logger = get_logger(__name__)

def run(job: str) -> None:
    if job == "test_discord":
        notification_service.send_test_message()
        return

    if job == "init_db":
        db_service.initialize()
        return

    # 테스트용 데이터 초기화, 실제 운영에서는 쓰지 말 것
    if job == "reset_db":
        db_service.reset_test_data()
        return

    if job == "sync_calendar":
        calendar_service.sync_events()
        return

    if job == "send_calendar_reminders":
        calendar_reminder_service.send_reminders()
        return

    if job == "collect_contents":
        content_collect_service.collect_rss_contents()
        return

    if job == "send_content_alerts":
        content_notification_service.send_immediate_alerts()
        return

    # 디스코드 봇 실행 (이 작업은 일반적으로 GitHub Actions에서 실행하지 않고, 로컬이나 별도의 서버에서 항상 켜두는 형태로 운영할 예정)
    if job == "run_discord_bot":
        from src.clients.discord_bot_client import run_bot
        run_bot()
        return

    raise ValueError(f"Unknown job: {job}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", required=True, help="실행할 작업 이름")
    args = parser.parse_args()

    logger.info("Job started: %s", args.job)
    run(args.job)
    logger.info("Job finished: %s", args.job)


if __name__ == "__main__":
    main()