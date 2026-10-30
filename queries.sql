-- 1. CTE: find available tables for 4 people on 1 Nov 2026, 19:00-21:00
WITH big_enough AS (
    -- Step 1: tables with enough seats
    SELECT id, restaurant_id, table_number, capacity
    FROM restaurant_tables
    WHERE capacity >= 4
),
busy AS (
    -- Step 2: tables with a booking that overlaps the requested time
    SELECT table_id
    FROM reservations
    WHERE status = 'confirmed'
      AND start_time < '2026-11-01 21:00'
      AND end_time > '2026-11-01 19:00'
)
-- Step 3: big enough AND not busy
SELECT r.name, r.city, b.table_number, b.capacity
FROM big_enough b
JOIN restaurants r ON r.id = b.restaurant_id
WHERE b.id NOT IN (SELECT table_id FROM busy)
ORDER BY r.name, b.capacity;


-- 2. RANK(): rank restaurants by average review score in each city
WITH averages AS (
    -- Step 1: one row per restaurant with its average rating
    SELECT r.name, r.city,
           ROUND(AVG(v.rating), 2) AS avg_rating,
           COUNT(*) AS review_count
    FROM restaurants r
    JOIN reviews v ON v.restaurant_id = r.id
    GROUP BY r.id, r.name, r.city
)
-- Step 2: rank them, starting again at 1 for each city
SELECT city, name, avg_rating, review_count,
       RANK() OVER (PARTITION BY city ORDER BY avg_rating DESC) AS city_rank
FROM averages
ORDER BY city, city_rank;
