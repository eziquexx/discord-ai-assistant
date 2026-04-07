from pathlib import Path
import sqlite3

from src.config.settings import settings

def get_connection() -> sqlite3.Connection:
    db_path = Path(settings.db_path)

    # data 폴더가 없으면 자동 생성
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row  # 결과를 dict 형태로 반환
    return connection