INSERT INTO artists (name)
VALUES
    ('Don Toliver'),
    ('Travis Scott'),
    ('Tame Impala');

INSERT INTO albums(artist_id, id, title, release_year)
VALUES
    (1, 1, 'Lovesick', 2023),
    (1, 2, 'HARDSTONE PSYCHO', 2024),
    (1, 3, 'OCTANE', 2026),
    (2, 1, 'ASTROWORLD', 2018),
    (2, 2, 'UTOPIA', 2023),
    (3, 1, 'Currents', 2015),
    (3, 2, 'The Slow Rush', 2020);

INSERT INTO songs (artist_id, album_id, title, duration_seconds, total_plays)
VALUES
    -- HARDSTONE PSYCHO
    (1, 2, 'NEW DROP', 217, 583410340),
    (1, 2, 'ROCKSTAR GIRL', 178, 17410056),

    -- Octane
    (1, 3, 'E85', 213, 356937135),

    -- UTOPIA
    (2, 2, 'MY EYES', 251, 864941956),
    (2, 2, 'I KNOW ?', 211, 968442476),

    -- The Slow Rush
    (3, 2, 'Borderline', 237, 1270087166);

INSERT INTO customers (name, email)
VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Charlie', 'charlie@example.com');

INSERT INTO purchases (customer_id, song_id, purchased_at)
VALUES
    (1, 1, '2026-09-20'),
    (1, 3, '2026-09-21'),
    (2, 1, '2026-09-22'),
    (3, 4, '2026-09-23');