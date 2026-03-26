create database if not exists cineflow_dw;

create schema if not exists cineflow_dw.raw;
create schema if not exists cineflow_dw.staging;
create schema if not exists cineflow_dw.analytics;

alter warehouse compute_wh resume if suspended;

--------------------------------------------------------------------
use database cineflow_dw;
use schema analytics;

create or replace table dim_user as
select 
    user_id,
    username,
    contact_num
from cineflow_dw.raw.users;

create or replace table dim_movie as
select 
    movie_id,
    movie_name,
    genre,
    duration,
    avg_ratings
from cineflow_dw.raw.movies;

create or replace table dim_theater as
select 
    s.screen_id,
    t.theater_id,
    t.theater_name,
    t.city,
    s.num_of_seats
from cineflow_dw.raw.screens s
join cineflow_dw.raw.theaters t
on s.theater_id = t.theater_id;

create or replace table fact_bookings as
select
    b.booking_id,
    b.user_id,
    st.movie_id,
    st.screen_id,
    b.num_of_tickets,
    b.total_amount,
    cast(to_timestamp(b.booking_time) as date) as booking_date,
    extract(month from to_timestamp(b.booking_time)) as booking_month,
    dayname(to_timestamp(b.booking_time)) as booking_dow
from cineflow_dw.raw.bookings b
join cineflow_dw.raw.showtime st
on b.show_id = st.show_id;

---------------------------------------------stream
-- Create a Snowake Stream called STR_BOOKINGS on STAGING.BOOKINGS that tracks any new rows 
-- inserted after each ETL run. Write a SELECT * FROM STR_BOOKINGS to see what the stream captures. 

create or replace stream str_bookings
on table cineflow_dw.raw.bookings;

select * from str_bookings;