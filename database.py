from datetime import date

import asyncpg

from config import DATABASE_URL

_pool: asyncpg.Pool | None = None


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
                created_at TEXT NOT NULL
            )
            """
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
    created_at = date.today().isoformat()
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
    today = date.today().isoformat()
    async with _pool.acquire() as conn:
        return await conn.fetchval(
            "SELECT COUNT(*) FROM registrations WHERE created_at = $1", today
        )


async def delete_all_registrations() -> int:
    async with _pool.acquire() as conn:
        result = await conn.execute("DELETE FROM registrations")
        await conn.execute("ALTER SEQUENCE registrations_id_seq RESTART WITH 1")
        return int(result.split()[-1])


async def save_user(telegram_id: int, username: str | None) -> None:
    first_seen = date.today().isoformat()
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
