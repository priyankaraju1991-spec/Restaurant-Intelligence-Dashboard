SHOW TABLES;
USE restaurant_db;
SELECT DATABASE();
SHOW TABLES;
SELECT *
FROM uber_eats_data
LIMIT 10;
SELECT COUNT(*) AS Total_Restaurants
FROM uber_eats_data;
DESCRIBE uber_eats_data;
SELECT name, rate
FROM uber_eats_data
ORDER BY rate DESC
LIMIT 10;
SELECT
    location,
    ROUND(AVG(rate), 2) AS average_rating
FROM uber_eats_data
GROUP BY location
ORDER BY average_rating DESC;
SELECT
    location,
    COUNT(*) AS total_restaurants
FROM uber_eats_data
GROUP BY location
ORDER BY total_restaurants DESC;
SELECT
    online_order,
    COUNT(*) AS total
FROM uber_eats_data
GROUP BY online_order;
SELECT
    book_table,
    COUNT(*) AS total
FROM uber_eats_data
GROUP BY book_table;
SELECT
    rest_type,
    COUNT(*) AS total
FROM uber_eats_data
GROUP BY rest_type
ORDER BY total DESC
LIMIT 10;
SELECT
    cuisines,
    COUNT(*) AS total
FROM uber_eats_data
GROUP BY cuisines
ORDER BY total DESC
LIMIT 10;
SELECT
    location,
    ROUND(AVG(`approx_cost(for two people)`), 2) AS average_cost
FROM uber_eats_data
GROUP BY location
ORDER BY average_cost DESC;
SELECT
    name,
    votes,
    rate
FROM uber_eats_data
WHERE votes > 1000
ORDER BY votes DESC;
SELECT
    name,
    votes
FROM uber_eats_data
ORDER BY votes DESC
LIMIT 10;
SELECT * FROM uber_eats_data LIMIT 10;
SELECT COUNT(*) FROM uber_eats_data;
DESCRIBE uber_eats_data;
SELECT name, rate FROM uber_eats_data ORDER BY rate DESC LIMIT 10;