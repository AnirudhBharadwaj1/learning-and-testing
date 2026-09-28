-- ==========================================
-- BASIC QUERIES
-- ==========================================

-- 1. Retrieve the names of all artists.
SELECT name
FROM artists;

-- 2. Retrieve all songs with more than 500,000,000 plays.
SELECT *
FROM songs
WHERE total_plays > 500000000;

-- 3. Retrieve all albums released after 2020,
--    ordered from newest to oldest.
SELECT *
FROM albums
WHERE release_year > 2020
ORDER BY release_year DESC;

-- 4. Retrieve the 3 most-played songs.
SELECT *
FROM songs
ORDER BY total_plays DESC
LIMIT 3;

-- 5. Retrieve all songs that are between 180 and 240 seconds long.
SELECT *
FROM songs
WHERE duration_seconds >= 180
AND duration_seconds <= 240;

-- ==========================================
-- AGGREGATION
-- ==========================================

-- 6. Count the total number of songs.
SELECT COUNT(*) AS num_songs
FROM songs;

-- 7. Find the total number of plays across all songs.
SELECT SUM(total_plays) AS total_plays
FROM songs;

-- 8. Find the average song duration.
SELECT AVG(duration_seconds) AS avg_duration
FROM songs;

-- 9. Find the number of songs released by each artist.
SELECT artist_id, COUNT(*) AS num_songs
FROM songs
GROUP BY artist_id;

-- 10. Find the total number of plays for each artist.
SELECT artist_id, SUM(total_plays) AS artist_total_plays
FROM songs
GROUP BY artist_id;

-- 11. Find artists who have more than 1 song.
SELECT artist_id, COUNT(*) AS num_songs
FROM songs
GROUP BY artist_id
HAVING COUNT(*) > 1;

-- 12. Find artists whose songs have more than 1,000,000,000
--     total plays.
SELECT artist_id
FROM songs
GROUP BY artist_id
HAVING SUM(total_plays) > 1000000000;

-- ==========================================
-- JOINS
-- ==========================================

-- 13. Retrieve every album along with the name of its artist.
SELECT al.title AS album_name, ar.name AS artist_name
FROM artists ar
JOIN albums al
ON ar.id = al.artist_id;

-- 14. Retrieve every song along with its album title.
SELECT s.title AS song_name, a.title AS album_name
FROM songs s
JOIN albums a
ON s.album_id = a.id
AND s.artist_id = a.artist_id;

-- 15. Retrieve every song along with its artist name and album title.
SELECT s.title AS song_name, al.title AS album_name, ar.name AS artist_name
FROM songs s
JOIN albums al
JOIN artists ar
ON s.album_id = al.id
AND s.artist_id = al.artist_id
AND s.artist_id = ar.id;

-- 16. Retrieve every customer and the songs they have purchased.
SELECT c.name, s.title
FROM customers c
JOIN purchases p
JOIN songs s
ON c.id = p.customer_id
AND p.song_id = s.id;

-- 17. Retrieve every artist, including artists who have no albums.
SELECT ar.name AS artist_name, a.title AS album_name
FROM artists ar
LEFT JOIN albums a
ON ar.id = a.artist_id;

-- 18. Retrieve every customer, including customers who have made
--     no purchases.
SELECT c.name AS customer_name, p.id AS purchase_id
FROM customers c
LEFT JOIN purchases p
ON c.id = p.customer_id;


-- ==========================================
-- SUBQUERIES
-- ==========================================

-- 19. Find all songs with more plays than the average song.
SELECT title
FROM songs
WHERE total_plays > (SELECT AVG(total_plays) FROM songs);

-- 20. Find all songs longer than the average song.
SELECT title
FROM songs
WHERE duration_seconds > (SELECT AVG(duration_seconds) FROM songs);

-- 21. Find the artist(s) with the most albums.
SELECT ar.name
FROM artists ar
JOIN albums al
ON al.artist_id = ar.id
GROUP BY ar.id, ar.name
HAVING COUNT(*) = (
    SELECT MAX(album_count)
    FROM (
        SELECT COUNT(*) AS album_count
        FROM albums
        GROUP BY artist_id
    )
);

-- 22. Find all songs belonging to the artist with the most albums.
SELECT s.*
FROM songs s
WHERE s.artist_id IN (
    SELECT artist_id
    FROM albums
    GROUP BY artist_id
    HAVING COUNT(*) = (
        SELECT MAX(album_count)
        FROM (
            SELECT COUNT(*) AS album_count
            FROM albums
            GROUP BY artist_id
        )
    )
);

-- 23. Find all songs that have never been purchased.
SELECT s.*
FROM songs s
WHERE NOT EXISTS (
    SELECT 1
    FROM purchases p
    WHERE p.song_id = s.id
);

-- 24. Find customers who have made at least one purchase.
SELECT c.*
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM purchases p
    WHERE p.customer_id = c.id
);

-- ==========================================
-- CTEs
-- ==========================================

-- 25. Using a CTE, calculate the total number of plays for each artist
--     and return the artists ordered by total plays.
WITH total_plays AS (
    SELECT artist_id, SUM(total_plays) AS num_plays
    FROM songs
    GROUP BY artist_id
)
SELECT a.name, t.num_plays
FROM artists a
JOIN total_plays t
ON a.id = t.artist_id;

-- 26. Using a CTE, calculate the number of songs on each album and
--     return albums containing more than 1 song.
WITH num_songs AS (
    SELECT artist_id, album_id, COUNT(*) AS song_count
    FROM songs
    GROUP BY artist_id, album_id
)
SELECT a.title, n.song_count
FROM albums a
JOIN num_songs n
ON a.artist_id = n.artist_id
AND a.id = n.album_id
WHERE n.song_count > 1;

-- 27. Using a CTE, calculate each customer's number of purchases and
--     return the customers ordered by purchase count.
WITH purchase_counts AS (
    SELECT customer_id, COUNT(*) AS purchase_count
    FROM purchases
    GROUP BY customer_id
)
SELECT c.name, pc.purchase_count
FROM customers c
JOIN purchase_counts pc
ON c.id = pc.customer_id
ORDER BY pc.purchase_count DESC;

-- 28. Using two CTEs, calculate both the total plays and average
--     song duration for each artist.
WITH total_plays AS (
    SELECT artist_id, SUM(total_plays) AS total_plays
    FROM songs
    GROUP BY artist_id
),
avg_duration AS (
    SELECT artist_id, AVG(duration_seconds) AS avg_duration
    FROM songs
    GROUP BY artist_id
)
SELECT ar.name, tp.total_plays, ad.avg_duration
FROM artists ar
JOIN total_plays tp
ON ar.id = tp.artist_id
JOIN avg_duration ad
ON ar.id = ad.artist_id;

-- ==========================================
-- CASE
-- ==========================================

-- 29. Classify each song as:
--     'Short'   (< 180 seconds)
--     'Medium'  (180-240 seconds)
--     'Long'    (> 240 seconds)
SELECT title,
    CASE
        WHEN duration_seconds < 180 THEN 'Short'
        WHEN duration_seconds > 240 THEN 'Long'
        ELSE 'Medium'
    END AS duration
FROM songs;

-- 30. Classify each song as:
--     'High'    (> 500,000,000 plays)
--     'Medium'  (100,000,000-500,000,000 plays)
--     'Low'     (everything else)
SELECT title,
    CASE
        WHEN total_plays > 500000000 THEN 'Viral'
        WHEN total_plays < 100000000 THEN 'Niche'
        ELSE 'Popular'
    END AS popularity
FROM songs;

-- 31. Count how many songs fall into each popularity category.


-- ==========================================
-- EXISTS
-- ==========================================

-- 32. Find all artists who have at least one song.
SELECT a.name
FROM artists a
WHERE EXISTS(
    SELECT 1
    FROM songs s
    WHERE s.artist_id = a.id
);

-- 33. Find all customers who have made at least one purchase.
SELECT c.name
FROM customers c
WHERE EXISTS(
    SELECT 1
    FROM purchases p
    WHERE p.customer_id = c.id
);

-- 34. Find all albums that contain at least one song.
SELECT a.title
FROM albums a
WHERE EXISTS(
    SELECT 1
    FROM songs s
    WHERE s.album_id = a.id
);

-- 35. Find all artists who have never released a song.
SELECT a.name
FROM artists a
WHERE NOT EXISTS(
    SELECT 1
    FROM songs s
    WHERE s.artist_id = a.id
);

-- ==========================================
-- UNION
-- ==========================================

-- 36. Return one list containing all artist names and customer names.
SELECT name
FROM artists
UNION
SELECT name
FROM customers;

-- 37. Return one list containing all album titles and song titles.
SELECT title
FROM albums
UNION
SELECT title
FROM songs;


-- ==========================================
-- WINDOW FUNCTIONS
-- ==========================================

-- 38. Rank all songs by total plays, with the most-played song ranked 1.
SELECT title, total_plays, RANK() OVER (ORDER BY total_plays DESC) AS rank
FROM songs;

-- 39. Assign a row number to each song ordered by total plays.
SELECT title, total_plays, ROW_NUMBER() OVER (ORDER BY total_plays DESC) AS row_num
FROM songs;

-- 40. For every song, display its total plays and the average plays
--     across all songs.
SELECT title, total_plays, AVG(total_plays) OVER () AS average_plays
FROM songs;

-- 41. Rank songs by total plays within each artist.
SELECT a.name, s.title, total_plays, RANK() OVER (
    PARTITION BY s.artist_id
    ORDER BY total_plays DESC
) AS artist_rank
FROM artists a
JOIN songs s
ON s.artist_id = a.id;

-- 42. Return the most-played song for each artist using a window function.
WITH ranked_songs AS (
    SELECT s.*, ROW_NUMBER() OVER (
        PARTITION BY artist_id
        ORDER BY total_plays DESC
    ) AS song_rank
    FROM songs s
)
SELECT *
FROM ranked_songs
WHERE song_rank = 1;

-- 43. Return the top 2 most-played songs for each artist.
WITH ranked_songs AS (
    SELECT s.*, ROW_NUMBER() OVER (
        PARTITION BY artist_id
        ORDER BY total_plays DESC
    ) AS song_rank
    FROM songs s
)
SELECT *
FROM ranked_songs
WHERE song_rank IN (1, 2);

-- ==========================================
-- MIXED / OA-STYLE
-- ==========================================

-- 44. Find the artist with the greatest total number of plays.
SELECT a.name, SUM(s.total_plays) AS total_plays
FROM artists a
JOIN songs s
ON s.artist_id = a.id
GROUP BY a.id, a.name
ORDER BY total_plays DESC
LIMIT 1;

-- 45. Find the album with the greatest total number of plays.
SELECT a.title, SUM(s.total_plays) AS total_plays
FROM albums a
JOIN songs s
ON a.artist_id = s.artist_id
AND a.id = s.album_id
GROUP BY a.artist_id, a.id, a.title
ORDER BY total_plays DESC
LIMIT 1;

-- 46. Find the customer who has purchased the most songs.
SELECT c.name, COUNT(p.song_id) AS num_purchases
FROM customers c
JOIN purchases p
ON c.id = p.customer_id
GROUP BY c.id, c.name
ORDER BY num_purchases DESC
LIMIT 1;

-- 47. Find all artists whose average song has more plays than the
--     overall average song.
SELECT a.name, AVG(s.total_plays) AS avg_plays
FROM artists a
JOIN songs s
ON a.id = s.artist_id
GROUP BY a.id, a.name
HAVING avg_plays > (
    SELECT AVG(total_plays)
    FROM songs
);

-- 48. For each artist, return their name, number of songs, average
--     song duration, and total plays.
SELECT
    a.name,
    COUNT(s.id) AS song_count,
    AVG(s.duration_seconds) AS avg_duration,
    SUM(s.total_plays) as total_plays
FROM artists a
JOIN songs s
ON a.id = s.artist_id
GROUP BY a.id, a.name;

-- 49. Return the top 3 artists ranked by their total song plays.
SELECT a.name, SUM(s.total_plays) AS total_plays
FROM artists a
JOIN songs s
ON a.id = s.artist_id
GROUP BY a.id, a.name
ORDER BY total_plays DESC
LIMIT 3;