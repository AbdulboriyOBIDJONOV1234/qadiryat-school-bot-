from datetime import datetime, timedelta, timezone

import asyncpg

from config import DATABASE_URL

_pool: asyncpg.Pool | None = None

UZT = timezone(timedelta(hours=5))


def now_uzt() -> str:
    return datetime.now(UZT).strftime("%Y-%m-%d %H:%M")


def format_dt(created_at: str) -> str:
    """'2026-06-16 14:30' → '16.06.2026 soat 14:30'"""
    try:
        dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M")
        return dt.strftime("%d.%m.%Y soat %H:%M")
    except ValueError:
        # eski format: '2026-06-16'
        try:
            dt = datetime.strptime(created_at, "%Y-%m-%d")
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            return created_at


async def init_db():
    global _pool
    _pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5, statement_cache_size=0)
    async with _pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS registrations (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT NOT NULL,
                username TEXT,
                full_name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                grade INTEGER NOT NULL,
                location TEXT NOT NULL,
                phone TEXT NOT NULL,
                created_at TEXT NOT NULL,
                reminded BOOLEAN DEFAULT FALSE
            )
            """
        )
        await conn.execute(
            "ALTER TABLE registrations ADD COLUMN IF NOT EXISTS reminded BOOLEAN DEFAULT FALSE"
        )
        await conn.execute(
            "ALTER TABLE registrations ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'pending'"
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bot_users (
                telegram_id BIGINT PRIMARY KEY,
                username TEXT,
                first_seen TEXT NOT NULL
            )
            """
        )


async def add_registration(telegram_id, username, full_name, birth_date, grade, location, phone) -> int:
    created_at = now_uzt()
    async with _pool.acquire() as conn:
        return await conn.fetchval(
            """
            INSERT INTO registrations
                (telegram_id, username, full_name, birth_date, grade, location, phone, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id
            """,
            telegram_id, username, full_name, birth_date, grade, location, phone, created_at,
        )


async def get_all_registrations():
    async with _pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, full_name, birth_date, grade, location, phone, created_at
            FROM registrations
            ORDER BY id
            """
        )
        return [tuple(row) for row in rows]


async def count_all() -> int:
    async with _pool.acquire() as conn:
        return await conn.fetchval("SELECT COUNT(*) FROM registrations")


async def count_today() -> int:
    today = datetime.now(UZT).strftime("%Y-%m-%d")
    async with _pool.acquire() as conn:
        return await conn.fetchval(
            "SELECT COUNT(*) FROM registrations WHERE created_at LIKE $1",
            f"{today}%",
        )


async def get_user_registrations(telegram_id: int):
    async with _pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, full_name, birth_date, grade, location, phone, created_at,
                   COALESCE(status, 'pending') AS status
            FROM registrations
            WHERE telegram_id = $1
            ORDER BY id
            """,
            telegram_id,
        )
        return [tuple(row) for row in rows]


async def get_registration_by_id(reg_id: int):
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, telegram_id, full_name, grade, phone FROM registrations WHERE id = $1",
            reg_id,
        )
        return tuple(row) if row else None


async def update_registration_status(reg_id: int, status: str) -> None:
    async with _pool.acquire() as conn:
        await conn.execute(
            "UPDATE registrations SET status = $1 WHERE id = $2", status, reg_id
        )


async def delete_all_registrations() -> int:
    async with _pool.acquire() as conn:
        result = await conn.execute("DELETE FROM registrations")
        await conn.execute("ALTER SEQUENCE registrations_id_seq RESTART WITH 1")
        return int(result.split()[-1])


async def save_user(telegram_id: int, username: str | None) -> None:
    first_seen = now_uzt()
    async with _pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO bot_users (telegram_id, username, first_seen)
            VALUES ($1, $2, $3)
            ON CONFLICT (telegram_id) DO NOTHING
            """,
            telegram_id, username, first_seen,
        )


async def get_all_user_ids() -> list[int]:
    async with _pool.acquire() as conn:
        rows = await conn.fetch("SELECT telegram_id FROM bot_users")
        return [row["telegram_id"] for row in rows]


async def count_users() -> int:
    async with _pool.acquire() as conn:
        return await conn.fetchval("SELECT COUNT(*) FROM bot_users")


async def count_this_week() -> int:
    now = datetime.now(UZT)
    monday = now - timedelta(days=now.weekday())
    week_start = monday.strftime("%Y-%m-%d")
    async with _pool.acquire() as conn:
        return await conn.fetchval(
            "SELECT COUNT(*) FROM registrations WHERE created_at >= $1",
            week_start,
        )


async def get_unreminded_registrations():
    """23–25 soat oldin tushgan, hali eslatilmagan arizalar."""
    now = datetime.now(UZT)
    window_start = (now - timedelta(hours=25)).strftime("%Y-%m-%d %H:%M")
    window_end = (now - timedelta(hours=23)).strftime("%Y-%m-%d %H:%M")
    async with _pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, full_name, grade, phone, created_at
            FROM registrations
            WHERE reminded = FALSE
              AND telegram_id != 0
              AND created_at >= $1
              AND created_at <= $2
            """,
            window_start, window_end,
        )
        return [tuple(row) for row in rows]


async def mark_reminded(reg_id: int) -> None:
    async with _pool.acquire() as conn:
        await conn.execute(
            "UPDATE registrations SET reminded = TRUE WHERE id = $1", reg_id
        )
