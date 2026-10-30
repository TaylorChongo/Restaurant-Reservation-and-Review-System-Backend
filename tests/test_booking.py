import threading

from booking import book_table

# From seed.sql: table 1 has 2 seats, table 2 has 4 seats
SMALL_TABLE = 1
TABLE = 2


def test_table_that_does_not_exist_is_refused():
    result = book_table(999999, 1, 2, "2030-01-01 19:00", "2030-01-01 21:00")
    assert result is None


def test_free_slot_is_booked():
    result = book_table(TABLE, 1, 4, "2030-01-01 19:00", "2030-01-01 21:00")
    assert isinstance(result, int)


def test_overlapping_booking_is_refused():
    book_table(TABLE, 1, 4, "2030-01-01 19:00", "2030-01-01 21:00")
    result = book_table(TABLE, 2, 2, "2030-01-01 20:00", "2030-01-01 22:00")
    assert result is None


def test_back_to_back_booking_is_allowed():
    book_table(TABLE, 1, 4, "2030-01-01 19:00", "2030-01-01 21:00")
    result = book_table(TABLE, 2, 2, "2030-01-01 21:00", "2030-01-01 23:00")
    assert isinstance(result, int)


def test_table_too_small_is_refused():
    result = book_table(SMALL_TABLE, 1, 5, "2030-01-01 19:00", "2030-01-01 21:00")
    assert result is None


def test_only_one_of_five_simultaneous_bookings_succeeds():
    starting_line = threading.Barrier(5)
    results = []

    def try_booking(customer_id: int) -> None:
        starting_line.wait()
        results.append(book_table(TABLE, customer_id, 2, "2030-01-01 19:00", "2030-01-01 21:00"))

    threads = []
    for i in range(5):
        t = threading.Thread(target=try_booking, args=((i % 4) + 1,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    successes = [r for r in results if r is not None]
    assert len(results) == 5
    assert len(successes) == 1
