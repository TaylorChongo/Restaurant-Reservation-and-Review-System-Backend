import threading

from booking import book_table

# 5 customers try to book the SAME table at the SAME time
NUMBER_OF_PEOPLE = 5
TABLE_ID = 5
START = "2026-11-02 19:00"
END = "2026-11-02 21:00"

# Makes all threads wait, then start together
starting_line = threading.Barrier(NUMBER_OF_PEOPLE)
results = []


def try_booking(customer_id: int) -> None:
    starting_line.wait()
    reservation_id = book_table(TABLE_ID, customer_id, 2, START, END)
    results.append(reservation_id)


threads = []
for i in range(NUMBER_OF_PEOPLE):
    customer_id = (i % 4) + 1  # we only have customers 1 to 4
    t = threading.Thread(target=try_booking, args=(customer_id,))
    threads.append(t)
    t.start()

# Wait for every thread to finish
for t in threads:
    t.join()

successes = [r for r in results if r is not None]
print("Results:", results)
print("Successful bookings:", len(successes))
