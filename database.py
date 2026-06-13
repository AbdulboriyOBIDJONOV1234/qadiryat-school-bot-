import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).parent / "registrations.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                username TEXT,
                full_name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                grade INTEGER NOT NULL,
                location TEXT NOT NULL,
                phone TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def add_registration(telegram_id, username, full_name, birth_date, grade, location, phone) -> int:
    created_at = date.today().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            INSERT INTO registrations
                (telegram_id, username, full_name, birth_date, grade, location, phone, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (telegram_id, username, full_name, birth_date, grade, location, phone, created_at),
        )
        conn.commit()
        return cursor.lastrowid


def get_all_registrations():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            SELECT id, full_name, birth_date, grade, location, phone, created_at
            FROM registrations
            ORDER BY id
            """
        )
        return cursor.fetchall()


def count_all() -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM registrations")
        return cursor.fetchone()[0]


def count_today() -> int:
    today = date.today().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT COUNT(*) FROM registrations WHERE created_at = ?", (today,)
        )
        return cursor.fetchone()[0]
