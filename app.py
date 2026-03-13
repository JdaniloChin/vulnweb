from flask import Flask, request
import sqlite3

app = Flask(__name__)

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

    user = request.args.get("user")
    password = request.args.get("pass")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # CONSULTA VULNERABLE
    query = f"SELECT * FROM users WHERE username='{user}' AND password='{password}'"

    result = cursor.execute(query).fetchall()

    conn.close()

    if result:
        return f"Login correcto: {result}"
    else:
        return "Login incorrecto"


if __name__ == "__main__":
    app.run()