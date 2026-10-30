from booking import book_table
from cache import is_table_available, redis_client

TABLE = 2
START = "2030-01-01 19:00"
END = "2030-01-01 21:00"
KEY = f"availability:{TABLE}:{START}:{END}"


def test_free_table_is_available_and_cached():
    assert is_table_available(TABLE, START, END) is True
    assert redis_client.get(KEY) == "1"


def test_cache_expires_after_60_seconds():
    is_table_available(TABLE, START, END)
    seconds_left = redis_client.ttl(KEY)
    assert 0 < seconds_left <= 60


def test_booking_clears_the_cache():
    is_table_available(TABLE, START, END)  # caches "free"
    book_table(TABLE, 1, 4, START, END)
    assert redis_client.get(KEY) is None


def test_booked_table_is_not_available():
    is_table_available(TABLE, START, END)  # caches "free"
    book_table(TABLE, 1, 4, START, END)
    assert is_table_available(TABLE, START, END) is False
