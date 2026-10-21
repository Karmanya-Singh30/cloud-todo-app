import os
import sqlite3
import tempfile
import unittest
from contextlib import closing
from unittest import mock

import app as app_module
from app import app, init_db

class TodoAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        # app.py reads DATABASE_PATH at import time, so replace the module value.
        self.db_patch = mock.patch.object(app_module, "DATABASE_PATH", self.temp_db.name)
        self.db_patch.start()
        init_db()
        app.config["TESTING"] = True
        self.client = app.test_client()
        with self.client.session_transaction() as session:
            session["csrf_token"] = "test-token"

    def tearDown(self):
        self.db_patch.stop()
        os.unlink(self.temp_db.name)

    def post(self, url, **data):
        data.setdefault("csrf_token", "test-token")
        return self.client.post(url, data=data, follow_redirects=True)

    def fetch_tasks(self):
        with closing(sqlite3.connect(self.temp_db.name)) as connection:
            return connection.execute("SELECT id, title, completed FROM tasks ORDER BY id").fetchall()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"My To-Do List", response.data)
        self.assertIn(b"Nothing on your list yet", response.data)

    def test_add_task(self):
        response = self.post("/add", title="  Finish report  ")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Finish report", response.data)
        self.assertEqual(self.fetch_tasks(), [(1, "Finish report", 0)])

    def test_add_rejects_empty_and_too_long_titles(self):
        self.assertIn(b"Please enter a task.", self.post("/add", title="   ").data)
        self.assertIn(b"200 characters or fewer", self.post("/add", title="x" * 201).data)
        self.post("/add", title="x" * 200)
        self.assertEqual(len(self.fetch_tasks()), 1)

    def test_title_is_html_escaped(self):
        response = self.post("/add", title="<script>alert(1)</script>")
        self.assertNotIn(b"<script>alert(1)</script>", response.data)
        self.assertIn(b"&lt;script&gt;", response.data)

    def test_toggle_task_both_ways(self):
        self.post("/add", title="Read notes")
        self.post("/toggle/1")
        self.assertEqual(self.fetch_tasks()[0][2], 1)
        self.post("/toggle/1")
        self.assertEqual(self.fetch_tasks()[0][2], 0)

    def test_edit_task(self):
        self.post("/add", title="Old title")
        response = self.post("/edit/1", title="New title")
        self.assertIn(b"Task updated.", response.data)
        self.assertEqual(self.fetch_tasks()[0][1], "New title")

    def test_edit_rejects_empty_title(self):
        self.post("/add", title="Keep me")
        response = self.post("/edit/1", title="")
        self.assertIn(b"Please enter a task.", response.data)
        self.assertEqual(self.fetch_tasks()[0][1], "Keep me")

    def test_delete_task(self):
        self.post("/add", title="Temporary")
        response = self.post("/delete/1")
        self.assertIn(b"Task deleted.", response.data)
        self.assertEqual(self.fetch_tasks(), [])

    def test_missing_task_returns_404(self):
        for url in ("/toggle/99", "/delete/99"):
            self.assertEqual(self.post(url).status_code, 404)
        self.assertEqual(self.post("/edit/99", title="x").status_code, 404)

    def test_post_without_csrf_token_is_rejected(self):
        response = self.post("/add", title="Sneaky", csrf_token="wrong")
        self.assertEqual(response.status_code, 400)
        response = self.client.post("/add", data={"title": "Sneaky"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.fetch_tasks(), [])

    def test_tasks_persist_across_init(self):
        self.post("/add", title="Survives restart")
        init_db()  # simulates app startup against an existing database
        self.assertEqual(self.fetch_tasks(), [(1, "Survives restart", 0)])

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok", "database": "ok"})

    def test_health_reports_database_failure(self):
        with mock.patch.object(app_module, "DATABASE_PATH", os.path.join(self.temp_db.name, "missing", "x.db")):
            response = self.client.get("/health")
        self.assertEqual(response.status_code, 503)

if __name__ == "__main__":
    unittest.main()
