-- =====================================
-- ADMIN USER
-- =====================================

INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$7qj7l6M3oZ2g5X9mOQ9M9ewK4w5l9j1gW5P3iLwVgJ6sQ6o1sR4mK',
    TRUE
);

-- =====================================
-- INITIAL AMENITIES
-- =====================================

INSERT INTO amenities (id, name)
VALUES
('f9b0bc2a-d733-4db7-bbbc-0d6f77af3fa1', 'WiFi'),
('f1b4d5c2-ff62-4622-aad8-4a6b8ebf8c2b', 'Swimming Pool'),
('9d1bdb2a-690d-4a74-a4ba-fb8c928ab835', 'Air Conditioning');
