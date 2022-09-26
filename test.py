import sqlite3

database = 'getbooked.db'
username = "Kie"


def user_lookup():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = cursor.execute(f'SELECT username FROM users').fetchall()
    for user in query:
        if username in user:
            print("found")
            break

        else:
            print("break")


user_lookup()