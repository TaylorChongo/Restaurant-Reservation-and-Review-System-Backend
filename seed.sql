-- Empty all tables and reset ids back to 1, so this file can be re-run
TRUNCATE reviews, reservations, restaurant_tables, customers, restaurants RESTART IDENTITY CASCADE;

-- 4 restaurants in 2 cities. POINT is (longitude, latitude)
INSERT INTO restaurants (name, city, location, menu, opening_hours) VALUES
('Nyamirambo Bites', 'Kigali', POINT(30.0450, -1.9780),
 '{"mains": ["Brochettes", "Isombe"], "drinks": ["Ikivuguto"]}',
 '{"mon-fri": "11:00-22:00", "sat-sun": "12:00-23:00"}'),
('Kimihurura Grill', 'Kigali', POINT(30.0870, -1.9500),
 '{"mains": ["Grilled Tilapia", "Sambaza"], "drinks": ["Primus"]}',
 '{"mon-sun": "16:00-23:00"}'),
('Volcano Kitchen', 'Musanze', POINT(29.6340, -1.4996),
 '{"mains": ["Matoke", "Ibihaza"], "drinks": ["Urwagwa"]}',
 '{"mon-sat": "10:00-21:00"}'),
('Lakeside Bistro', 'Musanze', POINT(29.6420, -1.5050),
 '{"mains": ["Ugali", "Goat Stew"], "drinks": ["African Tea"]}',
 '{"tue-sun": "12:00-22:00"}');

-- 3 tables per restaurant: seats 2, 4 and 6
INSERT INTO restaurant_tables (restaurant_id, table_number, capacity) VALUES
(1, 1, 2), (1, 2, 4), (1, 3, 6),
(2, 1, 2), (2, 2, 4), (2, 3, 6),
(3, 1, 2), (3, 2, 4), (3, 3, 6),
(4, 1, 2), (4, 2, 4), (4, 3, 6);

INSERT INTO customers (full_name, email, phone) VALUES
('Aline Uwase',      'aline@example.com', '0781111111'),
('Jean Mugisha',     'jean@example.com',  '0782222222'),
('Grace Ingabire',   'grace@example.com', '0783333333'),
('Eric Niyonzima',   'eric@example.com',  '0784444444');

-- A few existing bookings on 1 Nov 2026
INSERT INTO reservations (table_id, customer_id, party_size, start_time, end_time) VALUES
(2, 1, 4, '2026-11-01 19:00', '2026-11-01 21:00'),
(3, 2, 5, '2026-11-01 18:00', '2026-11-01 20:00'),
(8, 3, 3, '2026-11-01 19:30', '2026-11-01 21:30');

-- Star ratings (the long text will go in MongoDB later)
INSERT INTO reviews (restaurant_id, customer_id, rating) VALUES
(1, 1, 5), (1, 2, 4), (1, 3, 5),
(2, 1, 3), (2, 4, 4),
(3, 2, 4), (3, 3, 3),
(4, 4, 5), (4, 1, 4);
