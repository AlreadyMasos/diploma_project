import sqlite3 as sq

with sq.connect('alldata.db') as con:
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT
    )
    ''')
    name = (1,'masos')
    cur.execute('INSERT INTO users VALUES (?,?)',name)
    con.commit()
    b = cur.execute('''SELECT * FROM users''').fetchall()
    print(b)