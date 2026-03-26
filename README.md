# CineFlow

## Business Context
An online movie ticket booking platform like BookMyShow operates across multiple 
cities, allowing users to browse movies, select theaters, pick showtimes, book seats, and 
make payments. The platform also collects user reviews after each watch. The business 
wants to build a structured data pipeline that makes this data accessible for analysis — 
understanding revenue performance across movies, cities, and payment methods, and 
uncovering customer behaviour patterns such as repeat bookings, preferred genres, and 
peak booking times.

( Assume the price for each seat in a screen is same for each showtime but the price for seats 
in different screens could be different. )

## Assignment Problem Statement

### Section A — Git & GitHub
Initialize git-flow

Create a git hook for validating commit messages.

Commit requirements.txt  to the repo. What is the purpose of pinning library 
versions in a requirements.txt ?

### Section B — Database
Create a Class diagram for the given problem statement. It should contain all the 
required tables and the established relationships between them.

Design and create a PostgreSQL schema with the following 8 tables — users , 
movies , theaters , screens , showtimes , bookings , payments , reviews . Define 

appropriate data types, primary keys, foreign key constraints, and NOT NULL etc 
rules.

Create a Trigger that runs periodically to update the average rating of a movie 
based on user reviews.

Every time a customer opens the platform to browse available shows, the system 
queries the showtimes  table joined with bookings  to calculate remaining seats in real 
time. As historical data grows — thousands of past shows and millions of old 
bookings — this query scans rows that are completely irrelevant to a customer who 
just wants to see what is playing today or later. The goal is to give customers a fast, 
clean view of only upcoming, available shows without touching any historical data.

### Section C — Python
Write a Python script using the Faker  library to generate realistic synthetic data for 
all tables. Your script must respect foreign key relationships — no child record 
should reference a non-existent parent, no repeating records.

Create controllers for each table handling insertion and selection logic. Add 
validators for insertion operations. For e.g date format validators, type validators 
etc where needed.

Create a decorator that sits on top of each controller that creates logs of every 
activity in separate logs.txt  file.

Create a function that take a movie name as input and gives me all available 
showtimes.

( BONUS: Try to create a function which also lets me book tickets. )

### Section D — ETL & Snowflake
The screens  and theaters  tables are normalized in PostgreSQL but analysts never 
query them separately. During your ETL, write a single extract query that joins 
them into one denormalized DIM_THEATER  table and load it into Snowflake. Do the 
same for all other dimensions and design your Snowflake ANALYTICS  schema as a 
star schema with FACT_BOOKINGS  at the center and DIM_USER , DIM_MOVIE , and 
DIM_THEATER  as surrounding dimensions. Write the full DDL for FACT_BOOKINGS  — it 

should contain only surrogate keys pointing to dimension tables, measurable facts 
like num_seats  and total_amount , and derived columns like booking_month  and 
booking_dow  computed during ETL.

Create a Snowflake Stream called STR_BOOKINGS  on STAGING.BOOKINGS  that tracks any 
new rows inserted after each ETL run. Write a SELECT * FROM STR_BOOKINGS  to see what 
the stream captures. What are the three metadata columns Snowflake automatically 
adds to every stream?

Create a persistent table ANALYTICS.AGG_DAILY_REVENUE  with columns booking_date , 
total_bookings , total_revenue , and avg_booking_value . Write a task 
TSK_REFRESH_REVENUE_SUMMARY  that runs every midnight to insert new revenue details.
