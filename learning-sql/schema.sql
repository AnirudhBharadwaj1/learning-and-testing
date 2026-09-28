DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS albums;
DROP TABLE IF EXISTS artists;

CREATE TABLE artists (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE albums (
    id INTEGER,
    artist_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    release_year INTEGER,
    PRIMARY KEY (id, artist_id),
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

CREATE TABLE songs (
    id INTEGER PRIMARY KEY,
    artist_id INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    duration_seconds INTEGER,
    total_plays INTEGER,
    FOREIGN KEY (artist_id, album_id) REFERENCES albums(artist_id, id)
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE purchases (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    song_id INTEGER NOT NULL,
    purchased_at TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (song_id) REFERENCES songs(id)
);