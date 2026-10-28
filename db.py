import os

from dotenv import load_dotenv
from psycopg2 import pool
from psycopg2.extensions import connection

# Read the settings from the .env file
load_dotenv()

# Keep between 1 and 5 connections open and ready to use
connection_pool = pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=5,
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)


def get_connection() -> connection:
    """Borrow a connection from the pool."""
    return connection_pool.getconn()


def release_connection(conn: connection) -> None:
    """Give the connection back to the pool."""
    connection_pool.putconn(conn)


# Quick test: run "python db.py"
if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM restaurants;")
    print("Restaurants in database:", cur.fetchone()[0])
    cur.close()
    release_connection(conn)
