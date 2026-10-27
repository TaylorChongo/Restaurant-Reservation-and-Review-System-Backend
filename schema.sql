-- Drop old tables so this file can be re-run safely
DROP TABLE IF EXISTS reviews, reservations, restaurant_tables, customers, restaurants CASCADE;

CREATE TABLE restaurants (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    city          VARCHAR(100) NOT NULL,
    location      POINT NOT NULL,      -- (longitude, latitude)
    menu          JSONB,
    opening_hours JSONB
);

CREATE TABLE restaurant_tables (
    id            SERIAL PRIMARY KEY,
    restaurant_id INT NOT NULL REFERENCES restaurants(id),
    table_number  INT NOT NULL,
    capacity      INT NOT NULL CHECK (capacity > 0),
    UNIQUE (restaurant_id, table_number)
);

CREATE TABLE customers (
    id        SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email     VARCHAR(255) NOT NULL UNIQUE,
    phone     VARCHAR(20)
);

CREATE TABLE reservations (
    id          SERIAL PRIMARY KEY,
    table_id    INT NOT NULL REFERENCES restaurant_tables(id),
    customer_id INT NOT NULL REFERENCES customers(id),
    party_size  INT NOT NULL CHECK (party_size > 0),
    start_time  TIMESTAMP NOT NULL,
    end_time    TIMESTAMP NOT NULL,
    status      VARCHAR(20) NOT NULL DEFAULT 'confirmed'
                CHECK (status IN ('confirmed', 'cancelled')),
    CHECK (end_time > start_time)
);

CREATE TABLE reviews (
    id            SERIAL PRIMARY KEY,
    restaurant_id INT NOT NULL REFERENCES restaurants(id),
    customer_id   INT NOT NULL REFERENCES customers(id),
    rating        INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);
