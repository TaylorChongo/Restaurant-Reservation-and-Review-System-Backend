import pytest

from db import get_connection, release_connection
from reviews import add_review, get_reviews, reviews_collection


def get_rating(review_id: int):
    """Read one rating from PostgreSQL, or None if it does not exist."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT rating FROM reviews WHERE id = %s;", (review_id,))
        row = cur.fetchone()
    finally:
        cur.close()
        release_connection(conn)
    return None if row is None else row[0]


def test_review_is_saved_in_both_databases():
    review_id = add_review(1, 1, 4, "[TEST] Lovely food.")

    assert get_rating(review_id) == 4

    document = reviews_collection.find_one({"review_id": review_id})
    assert document["text"] == "[TEST] Lovely food."
    assert document["restaurant_id"] == 1


def test_get_reviews_returns_the_new_review():
    review_id = add_review(1, 1, 5, "[TEST] Great service.")
    review_ids = [review["review_id"] for review in get_reviews(1)]
    assert review_id in review_ids


def test_invalid_rating_saves_nothing():
    count_before = reviews_collection.count_documents({})

    with pytest.raises(Exception):
        add_review(1, 1, 6, "[TEST] Rating 6 is not allowed.")

    assert reviews_collection.count_documents({}) == count_before
