import pytest

from cache import redis_client
from db import get_connection, release_connection
from reviews import reviews_collection

# Tests only book on this day, and mark their reviews with this text,
# so we can find and delete everything they create
TEST_DAY = "2030-01-01"
TEST_REVIEW_MARK = "[TEST]"


def remove_test_data() -> None:
    """Delete everything the tests created in PostgreSQL, Redis and MongoDB."""
    # Find test reviews in MongoDB, so we know which ratings to delete
    test_reviews = list(reviews_collection.find({"text": {"$regex": "^\\[TEST\\]"}}))
    review_ids = [review["review_id"] for review in test_reviews]

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM reservations WHERE start_time >= %s;", (TEST_DAY,))
        if review_ids:
            cur.execute("DELETE FROM reviews WHERE id = ANY(%s);", (review_ids,))
        conn.commit()
    finally:
        cur.close()
        release_connection(conn)

    reviews_collection.delete_many({"review_id": {"$in": review_ids}})

    for key in redis_client.scan_iter("availability:*:2030-*"):
        redis_client.delete(key)


@pytest.fixture(autouse=True)
def clean_test_data():
    """Runs around every test: clean before, run the test, clean after."""
    remove_test_data()
    yield
    remove_test_data()
