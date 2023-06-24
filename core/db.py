import sqlite3
from schemas import RecordDto, RecordSettings


class Database:
    def __init__(self, filename: str = "data.db") -> None:

        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

    def __del__(self) -> None:
        self.conn.close()

    def create_table(self) -> None:
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_link TEXT,
            start_timecode TEXT,
            end_timecode TEXT,
            annotation_length INTEGER,
            article_length INTEGER,
            screenshot_timing INTEGER
            )"""
        )
        self.conn.commit()
