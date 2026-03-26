from utils.loggers import log_activity

@log_activity
def get_available_showtimes(cur, movie_name):
    query = """
        SELECT 
            m.movie_name,
            t.theater_name,
            t.city,
            s.screen_id,
            st.show_date,
            st.show_start_time,
            st.available_seats,
            st.price_per_seat
        FROM showtime st
        JOIN movies m ON st.movie_id = m.movie_id
        JOIN screens s ON st.screen_id = s.screen_id
        JOIN theaters t ON s.theater_id = t.theater_id
        WHERE 
            m.movie_name ILIKE %s
            AND st.show_date >= CURRENT_DATE
            AND st.available_seats > 0
        ORDER BY st.show_date, st.show_start_time;
    """

    cur.execute(query, (f"%{movie_name}%",))

    columns = [desc[0] for desc in cur.description]

    results = [dict(zip(columns, row)) for row in cur.fetchall()]

    return results