import sqlite3
from src.db.connection import get_connection


class BaseRepository:
    def get_connection(self) -> sqlite3.Connection:
        return get_connection()