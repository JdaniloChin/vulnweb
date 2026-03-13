from flask import Flask, request
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("database.db")


def init_db_if_needed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
        """
    )

    user_count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if user_count == 0:
        cursor.executemany(
            "INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
            [
                (1, "admin", "1234"),
                (2, "danilo", "sql123"),
                (3, "student", "pass"),
            ],
        )

    conn.commit()
    conn.close()


init_db_if_needed()

@app.route("/")
def home():

    return """
    <h2>Login</h2>

    <form action="/login">
        Usuario:<br>
        <input name="user"><br>

        Password:<br>
        <input name="pass"><br>

        <input type="submit">
    </form>
    """

@app.route("/login")
def login():

    user = request.args.get("user", "")
    password = request.args.get("pass", "")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # CONSULTA INTENCIONALMENTE VULNERABLE PARA DEMOSTRACION DE SQLi
    query = f"SELECT * FROM users WHERE username='{user}' AND password='{password}'"
    result = cursor.execute(query).fetchall()

    conn.close()

    if result:
        return f"Login correcto: {result}"
    else:
        return "Login incorrecto"

@app.route("/admin")
def admin():
    user = request.args.get("user","")
    conn =  sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Consulta Vulnerable
    query =  f"SELECT * FROM users WHERE username='{user}'"

    result = cursor.execute(query).fetchall()
    conn.close()

    if result and result[0][1] == "admin":
        return """
                <h1>Panel admin>/h1>
                <p>Usuarios del sistema:</p>
                """ + str(result)
    else:
        return "Acceso denegado"
    
@app.route("/view")
def view_file():
    file = request.args.get("file","")

    try:
        with open(file,"r") as f:
            content = f.read()

        return f"<pre>{content}</pre>"
    except:
        return "No se pudo abrir el archivo"

if __name__ == "__main__":
    app.run()