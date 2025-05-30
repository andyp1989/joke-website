from flask import Flask, jsonify, request, send_from_directory
import random
import sqlite3
from datetime import datetime
import openai
import os

app = Flask(__name__, static_folder='static')

# 🔑 Replace with your actual OpenAI key
openai.api_key = "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"

def get_db_connection():
    conn = sqlite3.connect('jokes.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            joke TEXT,
            rating TEXT,
            upvotes INTEGER,
            downvotes INTEGER,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def create_joke():
    ratings = ['G', 'PG', 'PG-13', 'R']
    rating = random.choice(ratings)

    prompt = f"Tell me a {rating}-rated, short joke. Only respond with the joke."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional joke writer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=60,
            temperature=0.9
        )
        joke = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        joke = "Oops! Couldn't generate a joke right now."

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO jokes (joke, rating, upvotes, downvotes, created_at) VALUES (?, ?, 0, 0, ?)",
                (joke, rating, datetime.now()))
    conn.commit()
    joke_id = cur.lastrowid
    conn.close()
    return {'id': joke_id, 'joke': joke, 'rating': rating, 'upvotes': 0, 'downvotes': 0}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/joke')
def get_joke():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jokes ORDER BY RANDOM() LIMIT 1")
    row = cur.fetchone()
    if row:
        result = dict(row)
    else:
        result = create_joke()
    conn.close()
    return jsonify(result)

@app.route('/api/vote', methods=['POST'])
def vote():
    data = request.get_json()
    joke_id = data.get('id')
    vote_type = data.get('type')

    if not joke_id or vote_type not in ['up', 'down']:
        return jsonify({'error': 'Invalid vote'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    if vote_type == 'up':
        cur.execute("UPDATE jokes SET upvotes = upvotes + 1 WHERE id = ?", (joke_id,))
    else:
        cur.execute("UPDATE jokes SET downvotes = downvotes + 1 WHERE id = ?", (joke_id,))

    conn.commit()
    conn.close()

    return jsonify({'success': True})

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Run the app (Render uses PORT env var)
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
