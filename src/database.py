import sqlite3

from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "ocr.db"

def _connect() -> sqlite3.Connection:
  connection = sqlite3.connect(DB_PATH)
  connection.row_factory = sqlite3.Row
  return connection

def initialize_database() -> None:
  DB_PATH.parent.mkdir(parents=True, exist_ok=True)

  with closing(_connect()) as connection:
      connection.execute("""
          CREATE TABLE IF NOT EXISTS texts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              series_id INTEGER NOT NULL,
              text TEXT NOT NULL
          )
      """)
      connection.execute("""
          CREATE TABLE IF NOT EXISTS series (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL
            )
      """)
      connection.commit()

def add_serie(name: str) -> dict[str, object]:    
    with closing(_connect()) as connection:
           cursor = connection.execute(
               "INSERT INTO series (name) VALUES (?)",
               (name),
           )
           connection.commit()
           return {"id": cursor.lastrowid, "name": name}

def get_series() -> list[dict[str, object]]:
    with closing(_connect()) as connection:
        rows = connection.execute(
            "SELECT id, name FROM series"
        ).fetchall()

        return [dict(row) for row in rows]

def add_text_by_serie(text: str, series_id: int) -> dict[str, object]:
    with closing(_connect()) as connection:
        cursor = connection.execute(
            "INSERT INTO texts (text) VALUES (?) WHERE series_id = ?",
            (text, series_id),
        )
        connection.commit()
        return {"id": cursor.lastrowid, "text": text}

def get_texts_by_serie(series_id: int) -> list[dict[str, object]]:
    with closing(_connect()) as connection:
        rows = connection.execute(
            "SELECT id, text FROM texts "
            "WHERE series_id = ? ORDER BY id ASC LIMIT ?",
            (series_id),
        ).fetchall()

        return [dict(row) for row in rows]