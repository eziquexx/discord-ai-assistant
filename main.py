import argparse

from src.services.notification_service import notification_service
from src.utils.logger import get_logger
from src.services.db_service import db_service

logger = get_logger(__name__)

def run(job: str) -> None:
    if job == "test_discord":
        notification_service.send_test_message()
        return

    if job == "init_db":
        db_service.initialize()
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