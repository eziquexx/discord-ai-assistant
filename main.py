import argparse

from src.utils.logger import get_logger

from src.jobs import (
    test_discord_job,
    init_db_job,
    reset_db_job,
    sync_calendar_job,
    send_calendar_reminders_job,
    collect_contents_job,
    send_content_alerts_job,
    run_discord_bot_job,
    send_daily_rss_digest_job,
)

logger = get_logger(__name__)

JOB_MAP = {
    "test_discord": test_discord_job.run,
    "init_db": init_db_job.run,
    "reset_db": reset_db_job.run,
    "sync_calendar": sync_calendar_job.run,
    "send_calendar_reminders": send_calendar_reminders_job.run,
    "collect_contents": collect_contents_job.run,
    "send_content_alerts": send_content_alerts_job.run,
    "run_discord_bot": run_discord_bot_job.run,
    "send_daily_rss_digest": send_daily_rss_digest_job.run,
}


def run(job: str) -> None:
    if job not in JOB_MAP:
        raise ValueError(f"Unknown job: {job}")
    JOB_MAP[job]()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", required=True, help="실행할 작업 이름")
    args = parser.parse_args()

    logger.info("Job started: %s", args.job)
    run(args.job)
    logger.info("Job finished: %s", args.job)


if __name__ == "__main__":
    main()