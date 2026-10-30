import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

from app.db import get_connection, release_connection

load_dotenv()

# Connect to MongoDB and pick the database and collection
mongo_client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
reviews_collection = mongo_client["reservation_db"]["reviews"]


def add_review(restaurant_id: int, customer_id: int, rating: int, text: str) -> int:
    """Save the rating in PostgreSQL and the long text in MongoDB."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        # 1. Save the rating in PostgreSQL (not committed yet)
        cur.execute(
            """
            INSERT INTO reviews (restaurant_id, customer_id, rating)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (restaurant_id, customer_id, rating),
        )
        review_id = cur.fetchone()[0]

        # 2. Save the long text in MongoDB, linked by review_id
        reviews_collection.insert_one({
            "review_id": review_id,
            "restaurant_id": restaurant_id,
            "customer_id": customer_id,
            "text": text,
            "created_at": datetime.now(),
        })

        # 3. Both saved, so make the PostgreSQL row permanent
        conn.commit()
        return review_id

    except Exception:
        # If MongoDB failed, this also removes the rating from step 1
        conn.rollback()
        raise

    finally:
        cur.close()
        release_connection(conn)


def get_reviews(restaurant_id: int) -> list[dict]:
    """Get all review texts for one restaurant from MongoDB."""
    return list(reviews_collection.find({"restaurant_id": restaurant_id}, {"_id": 0}))


# Quick test: run "python -m app.reviews" from the project folder
if __name__ == "__main__":
    new_id = add_review(1, 4, 5, "The brochettes were perfectly grilled and the staff were very friendly.")
    print("New review id:", new_id)

    for review in get_reviews(1):
        print(review)
