import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
)
""")

cursor.execute("INSERT INTO users VALUES (1,'admin','1234')")
cursor.execute("INSERT INTO users VALUES (2,'danilo','sql123')")
cursor.execute("INSERT INTO users VALUES (3,'student','pass')")

conn.commit()
conn.close()

print("Base creada")