-- movies table
create or replace table movies (
    movie_id serial primary key,
    movie_name varchar(200) not null,
    genre varchar(100),
    duration time,
    avg_ratings float
);

alter table movies
alter column avg_ratings drop default;

update movies
set avg_ratings = null
where avg_ratings = 0;

----------------------------------------------

-- users table
create table users (
    user_id serial primary key,
    username varchar(200) not null,
    contact_num varchar(15) not null unique
        check (contact_num ~ '^\+?[0-9]{10,15}$')
);

--------------------------------------------

-- theaters table
create table theaters (
    theater_id serial primary key,
    theater_name varchar(200) not null,
    city varchar(100) not null
);

--------------------------------------------------------

-- screens table
create table screens (
    screen_id serial primary key,
    theater_id integer not null,
    num_of_seats integer check (num_of_seats > 0),

    foreign key (theater_id)
    references theaters(theater_id)
    on delete cascade
);

------------------------------------------------------------------

-- showtime table
create table showtime (
    show_id serial primary key,
    movie_id integer not null,
    screen_id integer not null,
    show_date date not null,
    show_start_time time,
    available_seats integer check (available_seats >= 0),
    price_per_seat integer not null check (price_per_seat > 0),

    foreign key (movie_id)
    references movies(movie_id)
    on delete cascade,

    foreign key (screen_id)
    references screens(screen_id)
    on delete cascade
);

-------------------------------------------------------

-- bookings table
create table bookings (
    booking_id serial primary key,
    user_id integer not null,
    show_id integer not null,
    num_of_tickets integer check (num_of_tickets > 0),
    total_amount integer check (total_amount >= 0),
    booking_time timestamp default current_timestamp,

    foreign key (user_id)
    references users(user_id)
    on delete cascade,

    foreign key (show_id)
    references showtime(show_id)
    on delete cascade
);

--------------------------------------------------------

-- payments table
create table payments (
    payment_id serial primary key,
    booking_id integer not null unique,
    user_id integer not null,
    amount integer check (amount >= 0),
    payment_method varchar(50),

    foreign key (booking_id)
    references bookings(booking_id)
    on delete cascade,

    foreign key (user_id)
    references users(user_id)
    on delete cascade
);

--------------------------------------------

-- reviews table
create table reviews (
    review_id serial primary key,
    movie_id integer not null,
    user_id integer not null,
    booking_id integer unique,
    rating integer not null check (rating between 1 and 5),
    created_at timestamp default current_timestamp,

    foreign key (movie_id)
    references movies(movie_id)
    on delete cascade,

    foreign key (user_id)
    references users(user_id)
    on delete cascade,

    foreign key (booking_id)
    references bookings(booking_id)
    on delete set null
);


-----------------------------------trigger

-- Create a Trigger that runs to update the average rating of a movie based on user reviews.

create or replace function update_avg_rating()
returns trigger as $$
begin
    update movies
    set avg_ratings = (
        select avg(rating)
        from reviews
        where movie_id = coalesce(new.movie_id, old.movie_id)
    )
    where movie_id = coalesce(new.movie_id, old.movie_id);

    return null;
end;
$$ language plpgsql;

create trigger trg_update_avg_rating
after insert or update or delete
on reviews
for each row
execute function update_avg_rating();


------------------------materialized view

-- Every time a customer opens the platform to browse available shows, the system queries the showtimes table joined with bookings to
-- calculate remaining seats in real time. As historical data grows — thousands of past shows and millions of old
-- bookings — this query scans rows that are completely irrelevant to a customer who just wants to see what is playing today or later. 
-- The goal is to give customers a fast, clean view of only upcoming, available shows without touching any historical data

create materialized view upcoming_shows_mv as
select *
from showtime
where show_date >= current_date;

select * from upcoming_shows_mv;

select * from movies;
select * from users;
select * from theaters;
select * from screens;
select * from showtime;
select * from bookings;
select * from payments;
select * from reviews;

truncate table 
    reviews,
    payments,
    bookings,
    showtime,
    screens,
    theaters,
    users,
    movies
restart identity cascade;