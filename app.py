import os
import secrets
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from flask import Flask, abort, render_template, request, redirect, session, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this-key")
# Lax keeps the session (and its CSRF token) off cross-site POSTs.
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# SQLite database location can be overridden with DATABASE_PATH.
DATABASE_PATH = os.environ.get("DATABASE_PATH", str(Path(__file__).with_name("tasks.db")))
MAX_TITLE_LENGTH = 200

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

def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]

app.jinja_env.globals["csrf_token"] = csrf_token

@app.before_request
def check_csrf():
    if request.method == "POST":
        sent = request.form.get("csrf_token", "")
        if not sent or not secrets.compare_digest(sent, session.get("csrf_token", "")):
            abort(400, description="Your session expired. Reload the page and try again.")

def validate_title(title):
    """Return an error message for an invalid title, or None."""
    if not title:
        return "Please enter a task."
    if len(title) > MAX_TITLE_LENGTH:
        return f"Task must be {MAX_TITLE_LENGTH} characters or fewer."
    return None

def run_for_task(sql, params):
    """Execute a single-task statement and 404 if the task does not exist."""
    with get_db_connection() as connection:
        if connection.execute(sql, params).rowcount == 0:
            abort(404, description="That task no longer exists.")

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
        editing_id=request.args.get("edit", type=int),
        max_length=MAX_TITLE_LENGTH,
    )

@app.post("/add")
def add_task():
    title = request.form.get("title", "").strip()
    error = validate_title(title)
    if error:
        flash(error, "error")
    else:
        with get_db_connection() as connection:
            connection.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        flash("Task added successfully.", "success")
    return redirect(url_for("index"))

@app.post("/edit/<int:task_id>")
def edit_task(task_id):
    title = request.form.get("title", "").strip()
    error = validate_title(title)
    if error:
        flash(error, "error")
        return redirect(url_for("index", edit=task_id))
    run_for_task("UPDATE tasks SET title = ? WHERE id = ?", (title, task_id))
    flash("Task updated.", "success")
    return redirect(url_for("index"))

@app.post("/toggle/<int:task_id>")
def toggle_task(task_id):
    run_for_task(
        "UPDATE tasks SET completed = CASE completed WHEN 0 THEN 1 ELSE 0 END WHERE id = ?",
        (task_id,),
    )
    return redirect(url_for("index"))

@app.post("/delete/<int:task_id>")
def delete_task(task_id):
    run_for_task("DELETE FROM tasks WHERE id = ?", (task_id,))
    flash("Task deleted.", "success")
    return redirect(url_for("index"))

@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(error):
    return render_template("error.html", error=error), error.code

@app.get("/health")
def health():
    """Health-check endpoint for deployment monitoring; also verifies the database."""
    try:
        with get_db_connection() as connection:
            connection.execute("SELECT 1 FROM tasks LIMIT 1")
    except sqlite3.Error:
        return {"status": "error", "database": "unavailable"}, 503
    return {"status": "ok", "database": "ok"}, 200

# Create the database when the application starts.
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    # Debugger allows code execution, so it is opt-in and bound to localhost only.
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host="127.0.0.1" if debug else "0.0.0.0", port=port, debug=debug)
