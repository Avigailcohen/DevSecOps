from flask import Flask, request, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 
import random
import string
import re

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)

with app.app_context():
    db.create_all()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def is_valid_url(url):
    """בודק אם הקלט הוא URL תקף"""
    url_regex = re.compile(
        r'^(https?:\/\/)?' 
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6}|'  
        r'localhost|'  # או localhost
        r'\d{1,3}(\.\d{1,3}){3})'  # או כתובת IP
        r'(:\d+)?(\/[^\s]*)?$'  # פורט אופציונלי ושאר הנתיב
    )
    return re.match(url_regex, url) is not None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.json
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "No URL provided"}), 400

    # בדיקת תקינות ה-URL
    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    existing_url = URL.query.filter_by(original_url=original_url).first()
    if existing_url:
        return jsonify({"short_url": request.host_url + existing_url.short_url})

    short_url = generate_short_url()
    new_url = URL(original_url=original_url, short_url=short_url)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({"short_url": request.host_url + short_url})

@app.route("/<short_url>")
def redirect_to_original(short_url):
    url_entry = URL.query.filter_by(short_url=short_url).first()
    if url_entry:
        return redirect(url_entry.original_url)
    return jsonify({"error": "Short URL not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
