from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)
DB = "notes.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        """)

@app.route("/")
def home():
    with sqlite3.connect(DB) as conn:
        notes = conn.execute(
            "SELECT id, content FROM notes ORDER BY id DESC"
        ).fetchall()
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    content = request.form.get("content", "").strip()
    if content:
        with sqlite3.connect(DB) as conn:
            conn.execute(
                "INSERT INTO notes (content) VALUES (?)", (content,)
            )
    return redirect("/")

@app.route("/health")
def health():
    return {"status": "ok"}, 200

init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
