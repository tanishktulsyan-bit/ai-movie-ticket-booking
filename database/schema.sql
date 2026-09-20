-- database/schema.sql
-- AI-Based Movie Crowd Prediction System — Full Schema + Sample Data
-- Run this file once to initialise the database.

-- ─────────────────────────────────────────────
-- 1. Create & select the database
-- ─────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS movie_crowd_db;
USE movie_crowd_db;

-- ─────────────────────────────────────────────
-- 2. Drop tables in reverse-dependency order
--    (safe for re-runs)
-- ─────────────────────────────────────────────
DROP TABLE IF EXISTS CROWD_PREDICTION;
DROP TABLE IF EXISTS BOOKING;
DROP TABLE IF EXISTS CUSTOMER;
DROP TABLE IF EXISTS SHOW_DETAILS;
DROP TABLE IF EXISTS THEATRE;
DROP TABLE IF EXISTS MOVIE;

-- ─────────────────────────────────────────────
-- 3. MOVIE
-- ─────────────────────────────────────────────
CREATE TABLE MOVIE (
    movie_id    INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(150)   NOT NULL,
    genre       VARCHAR(80)    NOT NULL,
    language    VARCHAR(50)    NOT NULL,
    duration    INT            NOT NULL COMMENT 'Duration in minutes',
    rating      DECIMAL(3,1)   DEFAULT 0.0,
    release_date DATE          NOT NULL,
    created_at  TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────────
-- 4. THEATRE
-- ─────────────────────────────────────────────
CREATE TABLE THEATRE (
    theatre_id   INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(150)  NOT NULL,
    location     VARCHAR(200)  NOT NULL,
    total_seats  INT           NOT NULL,
    created_at   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────────
-- 5. SHOW_DETAILS
-- ─────────────────────────────────────────────
CREATE TABLE SHOW_DETAILS (
    show_id          INT AUTO_INCREMENT PRIMARY KEY,
    movie_id         INT          NOT NULL,
    theatre_id       INT          NOT NULL,
    show_date        DATE         NOT NULL,
    show_time        TIME         NOT NULL,
    ticket_price     DECIMAL(8,2) NOT NULL,
    available_seats  INT          NOT NULL,
    created_at       TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (movie_id)   REFERENCES MOVIE(movie_id)   ON DELETE CASCADE,
    FOREIGN KEY (theatre_id) REFERENCES THEATRE(theatre_id) ON DELETE CASCADE
);

-- ─────────────────────────────────────────────
-- 6. CUSTOMER
-- ─────────────────────────────────────────────
CREATE TABLE CUSTOMER (
    customer_id  INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    email        VARCHAR(150) NOT NULL UNIQUE,
    phone        VARCHAR(15)  NOT NULL,
    created_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────────
-- 7. BOOKING
-- ─────────────────────────────────────────────
CREATE TABLE BOOKING (
    booking_id    INT AUTO_INCREMENT PRIMARY KEY,
    show_id       INT          NOT NULL,
    customer_id   INT          NOT NULL,
    seats_booked  INT          NOT NULL,
    total_amount  DECIMAL(10,2) NOT NULL,
    booking_date  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    status        ENUM('confirmed','cancelled') DEFAULT 'confirmed',

    FOREIGN KEY (show_id)     REFERENCES SHOW_DETAILS(show_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id)  ON DELETE CASCADE
);

-- ─────────────────────────────────────────────
-- 8. CROWD_PREDICTION
-- ─────────────────────────────────────────────
CREATE TABLE CROWD_PREDICTION (
    prediction_id      INT AUTO_INCREMENT PRIMARY KEY,
    show_id            INT          NOT NULL,
    predicted_crowd    INT          NOT NULL,
    confidence_score   DECIMAL(5,2) NOT NULL COMMENT 'Percentage 0-100',
    crowd_level        ENUM('Low','Medium','High','Housefull') NOT NULL,
    prediction_date    TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (show_id) REFERENCES SHOW_DETAILS(show_id) ON DELETE CASCADE
);

-- ─────────────────────────────────────────────
-- 9. TRIGGER — reduce available_seats on booking
-- ─────────────────────────────────────────────
DELIMITER $$
DROP TRIGGER IF EXISTS after_booking_insert$$
CREATE TRIGGER after_booking_insert
AFTER INSERT ON BOOKING
FOR EACH ROW
BEGIN
    UPDATE SHOW_DETAILS
    SET    available_seats = available_seats - NEW.seats_booked
    WHERE  show_id = NEW.show_id;
END$$
DELIMITER ;

-- ─────────────────────────────────────────────
-- 10. SAMPLE DATA
-- ─────────────────────────────────────────────

-- Movies
INSERT INTO MOVIE (title, genre, language, duration, rating, release_date) VALUES
('Inception',          'Sci-Fi / Thriller', 'English', 148, 8.8, '2010-07-16'),
('KGF Chapter 2',      'Action / Drama',    'Kannada', 168, 8.4, '2022-04-14'),
('Pathaan',            'Action / Thriller', 'Hindi',   146, 7.4, '2023-01-25'),
('RRR',                'Action / Drama',    'Telugu',  182, 7.9, '2022-03-25'),
('Kalki 2898 AD',      'Sci-Fi / Action',   'Telugu',  180, 7.2, '2024-06-27'),
('Avengers Endgame',   'Superhero / Action','English', 181, 8.4, '2019-04-26');

-- Theatres
INSERT INTO THEATRE (name, location, total_seats) VALUES
('PVR Cinemas',      'Chennai - Express Avenue',  250),
('INOX Multiplex',   'Chennai - Phoenix Mall',    300),
('SPI Palazzo',      'Chennai - Palazzo Mall',    200),
('Rohini Theatre',   'Chennai - Koyambedu',       500),
('Vettri Multiplex', 'Chennai - Velachery',       350);

-- Shows
INSERT INTO SHOW_DETAILS (movie_id, theatre_id, show_date, show_time, ticket_price, available_seats) VALUES
(1, 1, '2024-08-10', '10:00:00', 250.00, 250),
(1, 2, '2024-08-10', '13:30:00', 300.00, 300),
(2, 3, '2024-08-11', '11:00:00', 200.00, 200),
(2, 4, '2024-08-11', '14:00:00', 150.00, 500),
(3, 5, '2024-08-12', '17:30:00', 280.00, 350),
(4, 1, '2024-08-12', '20:00:00', 260.00, 250),
(5, 2, '2024-08-13', '09:30:00', 320.00, 300),
(6, 3, '2024-08-13', '15:00:00', 350.00, 200),
(3, 4, '2024-08-14', '18:00:00', 180.00, 500),
(4, 5, '2024-08-14', '21:00:00', 240.00, 350);

-- Customers
INSERT INTO CUSTOMER (name, email, phone) VALUES
('Arjun Kumar',   'arjun@example.com',   '9876543210'),
('Priya Sharma',  'priya@example.com',   '9123456780'),
('Rahul Mehta',   'rahul@example.com',   '9988776655'),
('Sneha Iyer',    'sneha@example.com',   '9001122334'),
('Karthik Raj',   'karthik@example.com', '9445566778');

-- Bookings  (trigger will auto-reduce available_seats)
INSERT INTO BOOKING (show_id, customer_id, seats_booked, total_amount) VALUES
(1, 1,  5, 1250.00),
(1, 2,  3,  750.00),
(2, 3,  8, 2400.00),
(3, 4,  2,  400.00),
(4, 5, 10, 1500.00),
(5, 1,  4, 1120.00),
(6, 2,  6, 1560.00),
(7, 3,  7, 2240.00),
(8, 4,  3, 1050.00),
(9, 5, 12, 2160.00),
(1, 3, 20, 5000.00),
(2, 4, 15, 4500.00),
(4, 1, 50, 7500.00),
(5, 2, 30, 8400.00);