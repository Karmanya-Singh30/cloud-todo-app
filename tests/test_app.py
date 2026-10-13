import os
import tempfile
import unittest
from app import app, init_db

class TodoAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        os.environ["DATABASE_PATH"] = self.temp_db.name
        # app.py reads DATABASE_PATH at import time, so replace the module value too.
        import app as app_module
        app_module.DATABASE_PATH = self.temp_db.name
        init_db()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        import app as app_module
        try:
            os.unlink(self.temp_db.name)
        except FileNotFoundError:
            pass
        os.environ.pop("DATABASE_PATH", None)

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"My To-Do List", response.data)

    def test_add_task(self):
        response = self.client.post("/add", data={"title": "Finish report"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Finish report", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

if __name__ == "__main__":
    unittest.main()
