import os
import random
from datetime import datetime, timedelta
from pathlib import Path
import psycopg2
from faker import Faker
from dotenv import load_dotenv
from controllers.user_controller import insert_user
from controllers.movie_controller import insert_movie
from controllers.showtime_controller import get_available_showtimes

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

print("DB_USER:", os.getenv("DB_USER"))

fake = Faker()


#------------ dbconnection

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()


#---------------movies

def insert_movies(n=10):
    movie_ids = []
    for _ in range(n):
        movie_id = insert_movie(
            cur,
            fake.catch_phrase(),
            random.choice(['Action', 'Comedy', 'Drama', 'Sci-Fi']),
            f"{random.randint(1,3)}:{random.randint(0,59)}:00"
        )
        movie_ids.append(movie_id)
    return movie_ids



#----------------------users

def insert_users(n=20):
    user_ids = []
    used_numbers = set()

    for _ in range(n):
        phone = fake.msisdn()[:10]

        while phone in used_numbers:
            phone = fake.msisdn()[:10]

        used_numbers.add(phone)

        user_id = insert_user(cur, fake.name(), phone)
        user_ids.append(user_id)

    return user_ids


#--------------------------------theaters

def insert_theaters(n=5):
    theater_ids = []
    for _ in range(n):
        cur.execute("""
            INSERT INTO theaters (theater_name, city)
            VALUES (%s, %s)
            RETURNING theater_id
        """, (fake.company(), fake.city()))

        theater_ids.append(cur.fetchone()[0])

    return theater_ids



#------------------------------- screens

def insert_screens(theater_ids, n=10):
    screen_ids = []
    for _ in range(n):
        cur.execute("""
            INSERT INTO screens (theater_id, num_of_seats)
            VALUES (%s, %s)
            RETURNING screen_id
        """, (
            random.choice(theater_ids),
            random.randint(50, 200)
        ))

        screen_ids.append(cur.fetchone()[0])

    return screen_ids


#---------------------- showtimes
def insert_showtimes(movie_ids, screen_ids, n=20):
    show_ids = []
    for _ in range(n):
        cur.execute("""
            INSERT INTO showtime (
                movie_id, screen_id, show_date,
                show_start_time, available_seats, price_per_seat
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING show_id
        """, (
            random.choice(movie_ids),
            random.choice(screen_ids),
            datetime.now().date() + timedelta(days=random.randint(0, 5)),
            f"{random.randint(10,22)}:00:00",
            random.randint(20, 150),
            random.randint(100, 500)
        ))

        show_ids.append(cur.fetchone()[0])

    return show_ids


#-------------------------bookings

def insert_bookings(user_ids, show_ids, n=30):
    booking_ids = []
    for _ in range(n):
        tickets = random.randint(1, 5)
        price = random.randint(100, 500)

        cur.execute("""
            INSERT INTO bookings (
                user_id, show_id, num_of_tickets,
                total_amount, booking_time
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING booking_id
        """, (
            random.choice(user_ids),
            random.choice(show_ids),
            tickets,
            tickets * price,
            datetime.now()
        ))

        booking_ids.append(cur.fetchone()[0])

    return booking_ids


#--------------------payments
def insert_payments(booking_ids, user_ids):
    for booking_id in booking_ids:
        cur.execute("""
            INSERT INTO payments (
                booking_id, user_id, amount, payment_method
            )
            VALUES (%s, %s, %s, %s)
        """, (
            booking_id,
            random.choice(user_ids),
            random.randint(100, 2000),
            random.choice(['UPI', 'Card', 'Net Banking'])
        ))


#------------------------------------reviews

def insert_reviews(booking_ids, user_ids, movie_ids, n=20):
    used_booking = set()

    for _ in range(n):
        booking = random.choice(booking_ids)

        if booking in used_booking:
            continue

        used_booking.add(booking)

        cur.execute("""
            INSERT INTO reviews (
                movie_id, user_id, booking_id,
                rating, created_at
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            random.choice(movie_ids),
            random.choice(user_ids),
            booking,
            random.randint(1, 5),
            datetime.now()
        ))



try:
    print("\n Seed data...\n")

    movie_ids = insert_movies()
    user_ids = insert_users()
    theater_ids = insert_theaters()
    screen_ids = insert_screens(theater_ids)
    show_ids = insert_showtimes(movie_ids, screen_ids)
    booking_ids = insert_bookings(user_ids, show_ids)

    insert_payments(booking_ids, user_ids)
    insert_reviews(booking_ids, user_ids, movie_ids)

    conn.commit()
    print("Data inserted successfullY!")


#------call function
 
    movie_input = input("\n Enter movie name to search showtimes: ")

    shows = get_available_showtimes(cur, movie_input)

    if not shows:
        print("No available shows found.")
    else:
        print("\nAvailable Showtimes:\n")

        for show in shows:
            print(f"""
   Movie: {show['movie_name']}
   Theater: {show['theater_name']} ({show['city']})
   Screen: {show['screen_id']}
   Date: {show['show_date']}
   Time: {show['show_start_time']}
   Seats: {show['available_seats']}
   Price: ₹{show['price_per_seat']}
""")

except Exception as e:
    conn.rollback()
    print("Error:", e)

finally:
    cur.close()
    conn.close()


