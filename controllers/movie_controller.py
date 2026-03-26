from utils.loggers import log_activity

@log_activity
def insert_movie(cur, name, genre, duration):
    cur.execute("""
        INSERT INTO movies (movie_name, genre, duration)
        VALUES (%s, %s, %s)
        RETURNING movie_id
    """, (name, genre, duration))

    return cur.fetchone()[0]


@log_activity
def get_all_movies(cur):
    cur.execute("SELECT * FROM movies")
    return cur.fetchall()