import sqlite3


async def create_db():
    global conn, cur

    conn = sqlite3.connect('users_data.sql')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, status TEXT, prefer TEXT)")
    conn.commit()


async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users VALUES(?, ?, ?)", (user_id, '', ''))
        conn.commit()


async def edit_profile(user_id, status, prefer):
    cur.execute("UPDATE users SET status = '{}', prefer = '{}' WHERE user_id == '{}'".format(status, prefer, user_id))
    conn.commit()


def get_users():
    conn = sqlite3.connect('users_data.sql')
    cur = conn.cursor()
    result = cur.execute("SELECT user_id, prefer FROM users WHERE status == 'yes'").fetchall()
    return result