-- Indexes to speed up the availability query (queries.sql, query 1)

-- Time slots: lets Postgres jump straight to bookings around the requested time
CREATE INDEX IF NOT EXISTS idx_reservations_time
    ON reservations (start_time, end_time);

-- Table capacity: for "tables with at least N seats"
CREATE INDEX IF NOT EXISTS idx_tables_capacity
    ON restaurant_tables (capacity);

-- Location: GiST index for "restaurants near me" searches (queries.sql, query 4)
CREATE INDEX IF NOT EXISTS idx_restaurants_location
    ON restaurants USING GIST (location);

-- Update statistics so the planner knows about the new indexes
ANALYZE reservations;
ANALYZE restaurant_tables;
ANALYZE restaurants;
