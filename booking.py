from db import get_connection, release_connection


def book_table(table_id, customer_id, party_size, start_time, end_time):
    """Book a table if it is free. Returns the new reservation id, or None."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        # 1. Lock this table's row so nobody else can book it at the same time
        cur.execute(
            "SELECT capacity FROM restaurant_tables WHERE id = %s FOR UPDATE;",
            (table_id,),
        )
        row = cur.fetchone()
        if row is None:
            print("Table does not exist.")
            conn.rollback()
            return None

        # 2. Is the table big enough?
        capacity = row[0]
        if party_size > capacity:
            print("Table is too small for this party.")
            conn.rollback()
            return None

        # 3. Does a confirmed booking overlap the requested time?
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
        if cur.fetchone() is not None:
            print("Table is already booked at that time.")
            conn.rollback()
            return None

        # 4. The table is free, so save the booking
        cur.execute(
            """
            INSERT INTO reservations (table_id, customer_id, party_size, start_time, end_time)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (table_id, customer_id, party_size, start_time, end_time),
        )
        reservation_id = cur.fetchone()[0]
        conn.commit()
        return reservation_id

    except Exception:
        # Something went wrong: undo everything in this transaction
        conn.rollback()
        raise

    finally:
        # Always runs: close the cursor and return the connection to the pool
        cur.close()
        release_connection(conn)


# Quick test: run "python booking.py"
if __name__ == "__main__":
    # In seed.sql, table 2 is already booked from 19:00 to 21:00
    print(book_table(2, 4, 2, "2026-11-01 20:00", "2026-11-01 22:00"))  # overlaps
    print(book_table(2, 4, 2, "2026-11-01 21:00", "2026-11-01 23:00"))  # free
    print(book_table(1, 4, 5, "2026-11-01 12:00", "2026-11-01 14:00"))  # too small
