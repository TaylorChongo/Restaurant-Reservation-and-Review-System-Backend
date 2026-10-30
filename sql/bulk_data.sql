-- Adds a large amount of test data for performance testing.
-- Run seed.sql first, then this file once.

-- 1,000 extra restaurants in 5 cities, at random places in Rwanda
INSERT INTO restaurants (name, city, location, menu, opening_hours)
SELECT 'Restaurant ' || n,
       (ARRAY['Kigali', 'Musanze', 'Huye', 'Rubavu', 'Rwamagana'])[1 + n % 5],
       POINT(28.9 + random() * 2, -2.8 + random() * 1.8),
       '{"mains": ["Brochettes"]}',
       '{"mon-sun": "10:00-22:00"}'
FROM generate_series(1, 1000) AS n;

-- 10 tables for each new restaurant, with 2, 4, 6 or 8 seats
INSERT INTO restaurant_tables (restaurant_id, table_number, capacity)
SELECT r.id, t, (ARRAY[2, 4, 6, 8])[1 + t % 4]
FROM restaurants r
CROSS JOIN generate_series(1, 10) AS t
WHERE r.id > 4;

-- Every new table is booked 19:00-21:00 every evening for 30 days
INSERT INTO reservations (table_id, customer_id, party_size, start_time, end_time)
SELECT t.id,
       1 + (t.id + d) % 4,
       2,
       TIMESTAMP '2026-12-01 19:00' + d * INTERVAL '1 day',
       TIMESTAMP '2026-12-01 21:00' + d * INTERVAL '1 day'
FROM restaurant_tables t
CROSS JOIN generate_series(0, 29) AS d
WHERE t.id > 12;

-- Update Postgres's statistics so it can plan queries well
ANALYZE;
