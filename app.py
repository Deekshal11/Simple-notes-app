
import os
import sqlite3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

app.config["DATABASE"] = os.environ.get(
    "DATABASE_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes.db")
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Docker Notes App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef2ff;
            padding: 40px;
        }
        .card {
            max-width: 650px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
        }
        h1 { color: #2457d6; }
        input {
            padding: 12px;
            width: 70%;
        }
        button {
            padding: 12px;
            background: #2457d6;
            color: white;
            border: none;
            cursor: pointer;
        }
        li {
            background: #f1f5f9;
            padding: 12px;
            margin: 10px 0;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Docker Notes App</h1>
        <p>My web application running in a Docker container!</p>
        <form method="POST" action="/add">
            <input name="note" placeholder="Write a note..." required>
            <button type="submit">Add Note</button>
        </form>
        <h2>Saved Notes</h2>
        <ul>
        {% for note in notes %}
            <li>{{ note }}</li>
        {% else %}
            <li>No notes yet. Add your first note!</li>
        {% endfor %}
        </ul>
        <p><a href="/health">Check application health</a></p>
    </div>
</body>
</html>
"""


def get_db():
    return sqlite3.connect(app.config["DATABASE"])


def init_db():
    database_path = app.config["DATABASE"]
    os.makedirs(os.path.dirname(database_path) or ".", exist_ok=True)

    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        """)


init_db()


@app.route("/")
def home():
    with get_db() as db:
        rows = db.execute(
            "SELECT content FROM notes ORDER BY id DESC"
        ).fetchall()

    notes = [row[0] for row in rows]
    return render_template_string(HTML, notes=notes)


@app.route("/add", methods=["POST"])
def add_note():
    note = request.form.get("note", "").strip()

    if note:
        with get_db() as db:
            db.execute(
                "INSERT INTO notes (content) VALUES (?)",
                (note,)
            )

    return redirect("/")


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
