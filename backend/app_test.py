import unittest
import sqlite3
import os
from flask import Flask
from app import get_feedback  # Replace with actual import

app = Flask(__name__)
app.testing = True

# Register the route for testing
@app.route("/feedback")
def feedback_route():
    return get_feedback()

class FeedbackTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test database
        self.db_path = 'feedback.db'
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS feedback")
        cursor.execute("""
            CREATE TABLE feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment TEXT,
                rating INTEGER
            )
        """)
        cursor.executemany("INSERT INTO feedback (comment, rating) VALUES (?, ?)", [
            ("Great service", 5),
            ("Okay experience", 3),
            ("Poor support", 1)
        ])
        conn.commit()
        conn.close()
        self.client = app.test_client()

    def tearDown(self):
        os.remove(self.db_path)

    def test_get_all_feedback(self):
        response = self.client.get("/feedback")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 3)

    def test_filter_by_rating(self):
        response = self.client.get("/feedback?rating=5")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["rating"], 5)

    def test_sort_order(self):
        response = self.client.get("/feedback?sort=asc")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data[0]["rating"], 1)

    def test_invalid_sort_fallback(self):
        response = self.client.get("/feedback?sort=invalid")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data[0]["rating"], 5)  # Default to desc

    def test_sql_injection_attempt(self):
        response = self.client.get("/feedback?rating=5;DROP TABLE feedback")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(isinstance(data, list))  # Should not crash or drop table

if __name__ == "__main__":
    unittest.main()
