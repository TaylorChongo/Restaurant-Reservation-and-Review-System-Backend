import os

import redis
from dotenv import load_dotenv

from db import get_connection, release_connection

load_dotenv()

# Connect to Redis (Memurai on Windows). decode_responses gives us str, not bytes
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)

# How long a cached answer is trusted, in seconds
CACHE_SECONDS = 60


def is_table_available(table_id: int, start_time: str, end_time: str) -> bool:
    """Check if a table is free. Uses Redis first, then PostgreSQL."""
    key = f"availability:{table_id}:{start_time}:{end_time}"

    # 1. Is the answer already in Redis?
    cached = redis_client.get(key)
    if cached is not None:
        print("(answer from Redis)")
        return cached == "1"

    # 2. Not cached, so ask PostgreSQL
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT id FROM reservations
            WHERE table_id = %s
              AND status = 'confirmed'
              AND start_time < %s
              AND end_time > %s;
            """,
            (table_id, end_time, start_time),
        )
        available = cur.fetchone() is None
    finally:
        cur.close()
        release_connection(conn)

    # 3. Save the answer in Redis for next time ("1" = free, "0" = taken)
    print("(answer from PostgreSQL)")
    redis_client.set(key, "1" if available else "0", ex=CACHE_SECONDS)
    return available


def clear_table_cache(table_id: int) -> None:
    """Delete every cached time slot for one table."""
    for key in redis_client.scan_iter(f"availability:{table_id}:*"):
        redis_client.delete(key)


# Quick test: run "python cache.py"
if __name__ == "__main__":
    # Ask the same question twice
    print(is_table_available(6, "2026-11-03 19:00", "2026-11-03 21:00"))
    print(is_table_available(6, "2026-11-03 19:00", "2026-11-03 21:00"))
