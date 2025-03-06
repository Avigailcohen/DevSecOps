import pytest
from flask.testing import FlaskClient
from typing import Generator
import sys

sys.path.append("..")  # כדי לוודא שהייבוא של `app` יצליח גם מתוך `tests/`
from app import app  # ייבוא האפליקציה

@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:  
    """יוצר לקוח Flask לבדיקה"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client  # מחזיר לקוח Flask לבדיקה

def test_shorten_url(client):
    """בודק יצירת URL מקוצר תקין"""
    data = {"url": "https://example.com"}
    response = client.post("/shorten", json=data)

    assert response.status_code == 200
    json_data = response.get_json()
    assert "short_url" in json_data  # לוודא שהתגובה מכילה URL מקוצר

def test_shorten_invalid_url(client):
    """בודק מה קורה אם מנסים לקצר URL לא תקף"""
    invalid_urls = [
        {"url": ""},  # מחרוזת ריקה -> מחזיר "No URL provided"
        {"url": "1234567890"},  # רצף של מספרים בלבד -> מחזיר "Invalid URL"
        {"url": None},  # ערך ריק (None) -> מחזיר "No URL provided"
        {"url": "http://???///invalid-url"},  # URL עם תווים בלתי חוקיים -> מחזיר "Invalid URL"
    ]

    expected_errors = [
        "No URL provided",  # מחרוזת ריקה
        "Invalid URL",  # מספרים בלבד
        "No URL provided",  # None
        "Invalid URL",  # URL לא חוקי
    ]

    for i, invalid_data in enumerate(invalid_urls):
        response = client.post("/shorten", json=invalid_data)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["error"] == expected_errors[i]  # התאמה בין קלט להודעת שגיאה

def test_redirect_to_original(client):
    """בודק ניסיון לגשת ל-URL מקוצר"""
    response = client.get("/abcdef")  # בדיקה עבור URL אקראי
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["error"] == "Short URL not found"

def test_redirect_not_found(client):
    """בודק ניסיון לגשת ל-URL מקוצר שלא קיים"""
    response = client.get("/nonexistent123")
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["error"] == "Short URL not found"
