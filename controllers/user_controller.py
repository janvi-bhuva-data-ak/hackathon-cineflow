from utils.loggers import log_activity 

@log_activity
def insert_user(cur, username, contact_num):
    cur.execute("""
        INSERT INTO users (username, contact_num)
        VALUES (%s, %s)
        RETURNING user_id
    """, (username, contact_num))

    return cur.fetchone()[0]


@log_activity
def get_all_users(cur):
    cur.execute("SELECT * FROM users")
    return cur.fetchall()