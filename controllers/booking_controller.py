from utils.loggers import log_activity

@log_activity
def insert_booking(cur, user_id, show_id, tickets, amount):
    cur.execute("""
        INSERT INTO bookings (user_id, show_id, num_of_tickets, total_amount)
        VALUES (%s, %s, %s, %s)
        RETURNING booking_id
    """, (user_id, show_id, tickets, amount))

    return cur.fetchone()[0]


@log_activity
def get_all_bookings(cur):
    cur.execute("SELECT * FROM bookings")
    return cur.fetchall()