from db import get_connection, release_connection


def run_query(number: int) -> list[tuple]:
    """Run query number N from queries.sql and return its rows."""
    text = open("queries.sql", encoding="utf-8").read()
    # Each query starts with a title comment like "-- 1. ..."
    after_title = text.split(f"-- {number}.")[1]
    # Skip the rest of the title line
    query = after_title.split("\n", 1)[1]
    # Queries are separated by two blank lines
    query = query.split("\n\n\n")[0]

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
    finally:
        cur.close()
        release_connection(conn)
    return rows


def test_cte_skips_busy_tables():
    # Query 1: 4 people on 1 Nov 2026, 19:00-21:00
    rows = run_query(1)
    found = [(name, table_number) for name, city, table_number, capacity in rows]

    # Busy in seed.sql: Nyamirambo Bites tables 2 and 3, Volcano Kitchen table 2
    assert ("Nyamirambo Bites", 2) not in found
    assert ("Nyamirambo Bites", 3) not in found
    assert ("Volcano Kitchen", 2) not in found
    # Free and big enough
    assert ("Kimihurura Grill", 2) in found


def test_cte_only_returns_tables_big_enough():
    rows = run_query(1)
    for name, city, table_number, capacity in rows:
        assert capacity >= 4


def test_rank_puts_best_restaurant_first_in_each_city():
    # Query 2: rank restaurants by average rating per city
    rows = run_query(2)
    first_in_city = {}
    for city, name, avg_rating, review_count, city_rank in rows:
        if city_rank == 1:
            first_in_city[city] = name

    assert first_in_city["Kigali"] == "Nyamirambo Bites"
    assert first_in_city["Musanze"] == "Lakeside Bistro"


def test_nearest_restaurants_are_sorted_by_distance():
    # Query 4: the 5 restaurants nearest to central Kigali
    rows = run_query(4)
    distances = [distance for name, city, distance in rows]

    assert len(rows) == 5
    assert distances == sorted(distances)
