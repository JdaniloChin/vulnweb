from flask import Flask, request, render_template
import sqlite3, os
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
    return render_template("index.html")

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

    return render_template(
        "login_result.html",
        user=user,
        password=password,
        query=query,
        result=result,
        success=bool(result),
    )

@app.route("/admin")
def admin():
    user = request.args.get("user","")
    conn =  sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Consulta Vulnerable
    query =  f"SELECT * FROM users WHERE username='{user}'"

    result = cursor.execute(query).fetchall()
    conn.close()

    return render_template(
        "admin_result.html",
        user=user,
        query=query,
        result=result,
        allowed=bool(result and result[0][1] == "admin"),
    )
    
@app.route("/view")
def view_file():
    file = request.args.get("file","")
    content = ""
    error = ""

    try:
        with open(file,"r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as ex:
        error = str(ex)

    return render_template("view_result.html", file=file, content=content, error=error)
    

@app.route("/ping")
def ping():
    host = request.args.get("host","")
    ping_count_flag = "-n" if os.name == "nt" else "-c"
    command = f"ping {ping_count_flag} 1 {host}"

    output = os.popen(command).read()

    return render_template("ping_result.html", host=host, command=command, output=output)

if __name__ == "__main__":
    app.run()