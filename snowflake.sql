CREATE DATABASE IF NOT EXISTS CINEFLOW_DW;

CREATE SCHEMA IF NOT EXISTS CINEFLOW_DW.RAW;
CREATE SCHEMA IF NOT EXISTS CINEFLOW_DW.STAGING;
CREATE SCHEMA IF NOT EXISTS CINEFLOW_DW.ANALYTICS;

ALTER WAREHOUSE COMPUTE_WH RESUME IF SUSPENDED;


--------------------------------------------------------------------
USE DATABASE CINEFLOW_DW;
USE SCHEMA ANALYTICS;

CREATE OR REPLACE TABLE DIM_USER AS
SELECT 
    user_id,
    username,
    contact_num
FROM CINEFLOW_DW.RAW.USERS;


CREATE OR REPLACE TABLE DIM_MOVIE AS
SELECT 
    movie_id,
    movie_name,
    genre,
    duration,
    avg_ratings
FROM CINEFLOW_DW.RAW.MOVIES;


CREATE OR REPLACE TABLE DIM_THEATER AS
SELECT 
    s.screen_id,
    t.theater_id,
    t.theater_name,
    t.city,
    s.num_of_seats
FROM CINEFLOW_DW.RAW.SCREENS s
JOIN CINEFLOW_DW.RAW.THEATERS t
ON s.theater_id = t.theater_id;


CREATE OR REPLACE TABLE FACT_BOOKINGS AS
SELECT
    b.booking_id,
    b.user_id,
    st.movie_id,
    st.screen_id,
    b.num_of_tickets,
    b.total_amount,
    CAST(TO_TIMESTAMP(b.booking_time) AS DATE) AS booking_date,
    EXTRACT(MONTH FROM TO_TIMESTAMP(b.booking_time)) AS booking_month,
    DAYNAME(TO_TIMESTAMP(b.booking_time)) AS booking_dow
FROM CINEFLOW_DW.RAW.BOOKINGS b
JOIN CINEFLOW_DW.RAW.SHOWTIME st
ON b.show_id = st.show_id;

---------------------------------------------
CREATE OR REPLACE STREAM STR_BOOKINGS
ON TABLE CINEFLOW_DW.RAW.BOOKINGS;

SELECT * FROM STR_BOOKINGS;