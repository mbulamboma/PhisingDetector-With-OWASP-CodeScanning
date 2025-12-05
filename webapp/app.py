from flask import Flask, render_template, request, jsonify, session
import sqlite3
import joblib
import os
from datetime import datetime
import sys

# need to import our text processing stuff from the other folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'phishing_detector'))
from utils import clean_text, extract_numeric_features
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # TODO: change this!

# load our trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'phishing_detector', 'baseline_tfidf_lr.pkl')
model = joblib.load(MODEL_PATH)

# where we store chat messages
DB_PATH = 'chat.db'

def init_db():
    """Set up the database table if it doesn't exist yet"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            is_phishing INTEGER DEFAULT 0,
            phishing_probability REAL DEFAULT 0.0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def predict_phishing(message):
    """Check if a message looks like phishing"""
    # clean up the text first
    cleaned = clean_text(message)
    if not cleaned:
        cleaned = 'empty'  # fallback for empty messages
    
    # turn it into the format our model expects
    df = pd.DataFrame({'text': [cleaned]})
    
    # get all the numeric features (URLs, exclamation marks, etc)
    numeric = extract_numeric_features(df)
    
    # put text and numbers together for the model
    X = pd.concat([numeric.reset_index(drop=True), df[['text']].reset_index(drop=True)], axis=1)
    X['text'] = X['text'].fillna('empty').astype(str)
    
    # ask the model what it thinks
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]  # how sure is it that this is phishing?
    
    return int(prediction), float(probability)

@app.route('/')
def index():
    """Main chat page - give users a random name if they don't have one"""
    if 'username' not in session:
        session['username'] = f"User{datetime.now().strftime('%H%M%S')}"
    return render_template('chat.html', username=session['username'])

@app.route('/set_username', methods=['POST'])
def set_username():
    """Set username"""
    data = request.json
    username = data.get('username', '').strip()
    if username:
        session['username'] = username
        return jsonify({'success': True, 'username': username})
    return jsonify({'success': False, 'error': 'Invalid username'})

@app.route('/send_message', methods=['POST'])
def send_message():
    """Send a new message"""
    data = request.json
    message = data.get('message', '').strip()
    username = session.get('username', 'Anonymous')
    
    if not message:
        return jsonify({'success': False, 'error': 'Empty message'})
    
    # run it through our phishing detector
    is_phishing, probability = predict_phishing(message)
    
    # only flag it if we're pretty confident (>73%)
    is_high_confidence_phishing = is_phishing and probability > 0.73
    
    # Save to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (username, message, is_phishing, phishing_probability)
        VALUES (?, ?, ?, ?)
    ''', (username, message, int(is_high_confidence_phishing), probability))
    conn.commit()
    message_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'success': True,
        'message_id': message_id,
        'is_phishing': bool(is_high_confidence_phishing),
        'probability': probability
    })

@app.route('/get_messages', methods=['GET'])
def get_messages():
    """Get all messages"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username, message, is_phishing, phishing_probability, timestamp
        FROM messages
        ORDER BY timestamp ASC
    ''')
    messages = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'messages': [
            {
                'id': msg[0],
                'username': msg[1],
                'message': msg[2],
                'is_phishing': bool(msg[3]),
                'probability': msg[4],
                'timestamp': msg[5]
            }
            for msg in messages
        ]
    })

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    """Clear all messages"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    print("Starting up the chat app...")
    print(f"Using model: {MODEL_PATH}")
    print("Go to http://localhost:5000 to start chatting!")
    app.run(debug=True, port=5000)
