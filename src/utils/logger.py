# GitHub Actions log & Local Console log

import logging


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    # 이미 핸들러가 있으면 중복 추가하지 않도록 막는다.
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.propagate = False
    return logger