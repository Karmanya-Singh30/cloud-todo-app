import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this-key")

# SQLite database location can be overridden with DATABASE_PATH.
DATABASE_PATH = os.environ.get("DATABASE_PATH", str(Path(__file__).with_name("tasks.db")))

@contextmanager
def get_db_connection():
    """Open a connection, commit on success, and always close it."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

def init_db():
    """Create the tasks table if it does not exist."""
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/")
def index():
    with get_db_connection() as connection:
        tasks = connection.execute(
            "SELECT id, title, completed, created_at FROM tasks ORDER BY completed ASC, id DESC"
        ).fetchall()
    total = len(tasks)
    completed_count = sum(task["completed"] for task in tasks)
    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed_count=completed_count,
        pending_count=total - completed_count,
    )

@app.post("/add")
def add_task():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Please enter a task.", "error")
    elif len(title) > 200:
        flash("Task must be 200 characters or fewer.", "error")
    else:
        with get_db_connection() as connection:
            connection.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        flash("Task added successfully.", "success")
    return redirect(url_for("index"))

@app.post("/toggle/<int:task_id>")
def toggle_task(task_id):
    with get_db_connection() as connection:
        connection.execute(
            "UPDATE tasks SET completed = CASE completed WHEN 0 THEN 1 ELSE 0 END WHERE id = ?",
            (task_id,),
        )
    return redirect(url_for("index"))

@app.post("/delete/<int:task_id>")
def delete_task(task_id):
    with get_db_connection() as connection:
        connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    flash("Task deleted.", "success")
    return redirect(url_for("index"))

@app.get("/health")
def health():
    """Health-check endpoint for deployment monitoring."""
    return {"status": "ok"}, 200

# Create the database when the application starts.
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
