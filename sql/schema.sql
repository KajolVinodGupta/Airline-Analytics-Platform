CREATE DATABASE IF NOT EXISTS airline_analytics;
USE airline_analytics;

CREATE TABLE IF NOT EXISTS flight_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_date DATE,
    airline VARCHAR(50),
    flight_number VARCHAR(20),
    tail_number VARCHAR(20),

    origin_airport VARCHAR(10),
    origin_city VARCHAR(50),
    origin_state VARCHAR(50),

    destination_airport VARCHAR(10),
    destination_city VARCHAR(50),
    destination_state VARCHAR(50),

    dep_delay INT,
    arr_delay INT,
    distance INT,
    cancelled TINYINT,

    air_system_delay INT,
    security_delay INT,
    airline_delay INT,
    late_aircraft_delay INT,
    weather_delay INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales_data (
    id INT AUTO_INCREMENT PRIMARY KEY,

    flight_date DATE,
    airline VARCHAR(50),
    route VARCHAR(50),

    seats_sold INT,
    ticket_price FLOAT,
    revenue FLOAT,

    travel_class VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SHOW DATABASES;
USE airline_analytics;
SHOW TABLES;
DESCRIBE flight_history;
DESCRIBE sales_data;

DESCRIBE flight_delay;

SELECT COUNT(*) FROM flight_delay;

SHOW TABLES;

CREATE OR REPLACE VIEW flight_master AS
SELECT 
    f.flight_number,
    f.flight_date,
    f.airline AS airline_code,
    a.AIRLINE AS airline_name,
    f.origin,
    ap1.AIRPORT AS origin_name,
    f.destination,
    ap2.AIRPORT AS dest_name,
    f.dep_delay,
    f.arr_delay,
    f.distance
FROM flight_delay f
LEFT JOIN airlines a ON f.airline = a.iata_code
LEFT JOIN airports ap1 ON f.origin = ap1.iata_code
LEFT JOIN airports ap2 ON f.destination  = ap2.iata_code;

CREATE TABLE IF NOT EXISTS daily_delay_summary AS
SELECT
    flight_date,
    COUNT(*) AS total_flights,
    AVG(dep_delay) AS avg_dep_delay,
    AVG(arr_delay) AS avg_arr_delay
FROM flight_delay
GROUP BY flight_date
ORDER BY flight_date;

CREATE TABLE IF NOT EXISTS monthly_airline_performance AS
SELECT 
    airline,
    DATE_FORMAT(flight_date, '%Y-%m') AS month,
    COUNT(*) AS total_flights,
    AVG(arr_delay) AS avg_arr_delay,
    SUM(CASE WHEN arr_delay > 15 THEN 1 ELSE 0 END) AS delayed_flights
FROM flight_delay
GROUP BY airline, month
ORDER BY month;

CREATE TABLE IF NOT EXISTS airport_delay_rank AS
SELECT
    origin AS airport,
    AVG(dep_delay) AS avg_dep_delay,
    AVG(arr_delay) AS avg_arr_delay,
    COUNT(*) AS total_flights
FROM flight_delay
GROUP BY origin
ORDER BY avg_dep_delay DESC;

CREATE TABLE IF NOT EXISTS route_performance AS
SELECT
    origin,
    destination,
    COUNT(*) AS total_flights,
    AVG(dep_delay) AS avg_dep_delay,
    AVG(arr_delay) AS avg_arr_delay
FROM flight_delay
GROUP BY origin, destination;

SHOW TABLES;

USE airline_analytics;
SHOW TABLES;

SELECT COUNT(*) FROM flight_delay;
SELECT COUNT(*) FROM sales_data;

DESCRIBE flight_delay;

SELECT * FROM flight_master LIMIT 20;

CREATE TABLE IF NOT EXISTS flight_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_date DATE,
    airline VARCHAR(50),
    flight_number VARCHAR(15),
    origin VARCHAR(10),
    destination VARCHAR(10),
    dep_delay INT,
    arr_delay INT,
    distance INT,
    cancelled TINYINT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS live_flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(15),
    airline VARCHAR(50),
    departure_airport VARCHAR(50),
    arrival_airport VARCHAR(50),
    status VARCHAR(20),
    delay INT,
    latitude FLOAT,
    longitude FLOAT,
    timestamp DATETIME
);

CREATE TABLE IF NOT EXISTS sales_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_date DATE,
    route VARCHAR(50),
    seats_sold INT,
    ticket_price FLOAT,
    revenue FLOAT,
    class VARCHAR(20),
    airline VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS airport_info (
    iata VARCHAR(10) PRIMARY KEY,
    airport_name VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE IF NOT EXISTS airline_info (
    airline_code VARCHAR(10) PRIMARY KEY,
    airline_name VARCHAR(100),
    country VARCHAR(100)
);

SELECT COUNT(*) FROM flight_history;

CREATE OR REPLACE VIEW delay_summary_view AS
SELECT
    flight_date,
    airline,
    AVG(dep_delay) AS avg_dep_delay,
    AVG(arr_delay) AS avg_arr_delay,
    SUM(cancelled) AS total_cancelled
FROM flight_history
GROUP BY flight_date, airline
ORDER BY flight_date;

CREATE OR REPLACE VIEW sales_summary_view AS
SELECT
    flight_date,
    airline,
    SUM(revenue) AS total_revenue,
    SUM(seats_sold) AS total_seats_sold
FROM sales_data
GROUP BY flight_date, airline
ORDER BY flight_date;

CREATE OR REPLACE VIEW revenue_vs_delay_view AS
SELECT 
    f.flight_date,
    f.origin_airport AS origin,
    f.destination_airport AS destination,
    f.arr_delay,
    s.revenue
FROM flight_history f
JOIN sales_data s
    ON f.flight_date = s.flight_date
    AND CONCAT(f.origin_airport, '-', f.destination_airport) = s.route;

SELECT
    flight_date,
    AVG(dep_delay) AS avg_dep_delay,
    AVG(arr_delay) AS avg_arr_delay,
    SUM(cancelled) AS cancellations
FROM flight_history
GROUP BY flight_date
ORDER BY flight_date;

SELECT 
    origin_airport AS origin,
    destination_airport AS destination,
    AVG(arr_delay) AS avg_arr_delay
FROM flight_history
GROUP BY origin, destination
ORDER BY avg_arr_delay DESC
LIMIT 10;

SELECT 
    airline, 
    SUM(revenue) AS total_revenue
FROM sales_data
GROUP BY airline
ORDER BY total_revenue DESC;

SELECT 
    route,
    SUM(revenue) AS total_revenue
FROM sales_data
GROUP BY route
ORDER BY total_revenue DESC;

SELECT
    DATE_FORMAT(flight_date, '%Y-%m-01') AS month,
    SUM(revenue) AS monthly_revenue
FROM sales_data
GROUP BY month
ORDER BY month;

SELECT
    DATE_FORMAT(flight_date, '%Y-%m-01') AS month,
    AVG(arr_delay) AS avg_monthly_delay
FROM flight_history
GROUP BY month
ORDER BY month;

SELECT
    flight_date,
    airline,
    origin_airport AS origin,
    destination_airport AS destination,
    dep_delay,
    arr_delay,
    distance,
    cancelled
FROM flight_history;

SELECT
    DATE_FORMAT(flight_date, '%Y-%m-01') AS month,
    SUM(revenue) AS revenue
FROM sales_data
GROUP BY month
ORDER BY month;

USE airline_analytics;

SELECT COUNT(*) FROM flight_delay;
SELECT COUNT(*) FROM sales_data;
SELECT COUNT(*) FROM flight_history;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/sales_data.csv'
INTO TABLE sales_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(flight_date, airline, @dummy1, @dummy2, @dummy3, route, seats_sold, ticket_price, revenue, @travel_class)
SET travel_class = @travel_class;

SELECT COUNT(*) FROM sales_data;

SELECT * FROM sales_data;
SELECT * FROM flight_delay;
