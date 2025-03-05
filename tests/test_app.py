import unittest
import pytest
import json
import sys
import os 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app

#from app import app, db, URL, generate_short_url, is_valid_url

class TestUtils(unittest.TestCase):
    def test_generate_short_url_length(self):
        """בודק אם הקישור המקוצר הוא באורך 6"""
        short_url = generate_short_url()
        self.assertEqual(len(short_url), 6)

    def test_is_valid_url(self):
        """בודק אם ה-URL תקף"""
        self.assertTrue(is_valid_url("https://example.com"))
        self.assertTrue(is_valid_url("http://example.com"))
        self.assertFalse(is_valid_url("example"))
        self.assertFalse(is_valid_url("ftp://example.com"))

class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        """מכין סביבת בדיקות עם מסד נתונים זמני"""
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # מסד נתונים זמני
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """מנקה את מסד הנתונים אחרי כל טסט"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_shorten_valid_url(self):
        """בודק קיצור כתובת תקינה"""
        response = self.client.post("/shorten", json={"url": "https://example.com"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("short_url", data)

    def test_shorten_invalid_url(self):
        """בודק טיפול בקישור לא תקין"""
        response = self.client.post("/shorten", json={"url": "example"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "Invalid URL")

    def test_redirect_existing_short_url(self):
        """בודק הפניה מקישור מקוצר"""
        with app.app_context():
            new_url = URL(original_url="https://example.com", short_url="abcdef")
            db.session.add(new_url)
            db.session.commit()

        response = self.client.get("/abcdef")
        self.assertEqual(response.status_code, 302)  # 302 = הפניה

    def test_redirect_non_existing_short_url(self):
        """בודק ניסיון להיכנס לקישור מקוצר שלא קיים"""
        response = self.client.get("/nonexist")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["error"], "Short URL not found")

# לא צריך את השורה הבאה כי pytest לוקח את ניהול הבדיקות
# אם אתה רוצה להריץ את זה עם pytest, פשוט הרץ את pytest במקום להפעיל unittest.main()