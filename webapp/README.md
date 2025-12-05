# Chat App with Phishing Detection

A simple web chat that automatically checks messages for phishing attempts.

## What It Does

- Provides a basic chat interface
- Runs every message through the phishing detection model
- Warns users when suspicious messages are detected
- Stores chat history in a local database
- Shows some basic stats about detection

## Setup

1. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Make sure you have a trained model:**
   The app looks for `../phishing_detector/baseline_tfidf_lr.pkl`
   
   If you don't have this, go train one first:
   ```bash
   cd ../phishing_detector
   python train_baseline.py
   ```

3. **Run the app:**
   ```bash
   python app.py
   ```
   
4. **Open your browser:**
   Go to http://localhost:5000

## How It Works

When someone sends a message:
1. The app cleans the text (removes weird formatting)
2. Extracts features (URLs, punctuation patterns, etc.)
3. Runs it through the trained model
4. If confidence > 73%, marks it as suspicious
5. Stores everything in the SQLite database

## Files

- `app.py` - main Flask application
- `chat.html` - web interface 
- `requirements.txt` - Python dependencies
- `chat.db` - SQLite database (created automatically)

## Features

**Chat Interface:**
- Set your username
- Send messages
- See all previous messages
- Auto-refresh every 3 seconds
- Clear chat history

**Phishing Detection:**
- Real-time scanning
- Visual warnings for suspicious messages  
- Probability scores
- Conservative flagging (only high confidence)

**Database:**
- Stores all messages with timestamps
- Records phishing predictions and scores
- SQLite (no setup required)

## Customization

You can modify these in `app.py`:

```python
# Change confidence threshold for flagging
is_high_confidence_phishing = is_phishing and probability > 0.73

# Change auto-refresh rate (milliseconds)
// In the HTML template
setInterval(loadMessages, 3000);

# Change secret key (important for production!)
app.secret_key = 'your-secret-key-change-this-in-production'
```

## Demo Ideas

Try sending these types of messages to test the detection:

**Safe messages:**
- "Hey, how's your day going?"
- "Meeting is at 3pm in conference room B"
- "Can you review this document when you get a chance?"

**Phishing-like messages:**  
- "URGENT! Your account will be suspended unless you click here immediately!"
- "Congratulations! You've won $10,000! Call this number now!"
- "Your password has expired. Update it at this link to avoid account closure."

## Production Notes

This is a demo app - don't use it in production without:
- Changing the secret key
- Adding user authentication
- Adding input validation/sanitization  
- Setting up proper logging
- Using a real database (PostgreSQL, etc.)
- Adding HTTPS
- Rate limiting

## Troubleshooting

**"Model not found"**: Make sure you've trained a model first in the phishing_detector folder

**"Module not found"**: Install requirements with `pip install -r requirements.txt`

**"Permission denied on chat.db"**: Make sure the app can write files in the current directory

**App won't start**: Check that port 5000 isn't already in use

If you haven't trained it yet:
```bash
cd ../phishing_detector
python train_baseline.py --input ../Phishing_Email.csv
```

### 3. Run the Application

```bash
python app.py
```

### 4. Open Browser

Navigate to: **http://localhost:5000**

## 📁 Project Structure

```
webapp/
├── app.py                  # Flask application (backend)
├── templates/
│   └── chat.html          # Chat interface (frontend)
├── requirements.txt       # Python dependencies
├── chat.db               # SQLite database (auto-created)
└── README.md             # This file
```

## 🎨 How It Works

### Backend (app.py)

1. **Loads Model**: Imports your trained phishing detector
2. **SQLite Database**: Stores messages with phishing predictions
3. **API Endpoints**:
   - `GET /` - Chat page
   - `POST /send_message` - Send and scan message
   - `GET /get_messages` - Retrieve all messages
   - `POST /set_username` - Change username
   - `POST /clear_chat` - Clear all messages

### Message Processing

```
User sends message
    ↓
Clean text (remove HTML, normalize)
    ↓
Extract features (URLs, !, $, etc.)
    ↓
ML Model prediction
    ↓
Save to database with prediction
    ↓
Alert user if phishing detected
```

### Frontend (chat.html)

- **Modern UI**: Gradient design with smooth animations
- **Color Coding**:
  - Blue messages = Safe ✅
  - Red messages = Phishing ⚠️
- **Auto-refresh**: Polls server every 3 seconds for new messages
- **Interactive**: Change username, refresh, clear chat

## 🗄️ Database Schema

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    is_phishing INTEGER DEFAULT 0,
    phishing_probability REAL DEFAULT 0.0,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

## 🔧 Configuration

### Change Port

In `app.py`, line 147:
```python
app.run(debug=True, port=5000)  # Change port here
```

### Change Secret Key

In `app.py`, line 14:
```python
app.secret_key = 'your-secret-key-change-this-in-production'
```

### Adjust Auto-refresh Rate

In `chat.html`, line 261:
```javascript
setInterval(loadMessages, 3000);  // 3000ms = 3 seconds
```

## 📊 Features Explained

### Phishing Detection

When a message is sent:
1. Model analyzes text content
2. Checks for suspicious patterns (URLs, urgent language, etc.)
3. Returns prediction + confidence score
4. Displays warning if phishing probability > 50%

### Statistics

Shows real-time stats:
- Total messages sent
- Number of phishing messages detected
- Detection percentage

### User Alerts

When phishing is detected:
```
⚠️ WARNING: This message has been flagged as potentially phishing!

Confidence: 87.3%

Please review suspicious links or requests for sensitive information.
```

## 🛡️ Security Notes

**For Educational/Demo Use:**
- No authentication system
- No encryption
- Sessions stored in cookies
- Single user simulation

**For Production:**
- Add user authentication
- Implement HTTPS
- Use proper session management
- Add input validation
- Implement rate limiting

## 🎓 Technical Details

### Why No Real-time?

This app uses **polling** instead of WebSockets/Socket.IO:
- ✅ Simpler setup (no additional libraries)
- ✅ Works everywhere (no special server requirements)
- ✅ Good enough for demo/educational purposes
- Auto-refreshes every 3 seconds

### Model Integration

The app:
1. Imports `utils.py` from phishing_detector
2. Uses same feature extraction as training
3. Ensures consistency between training and inference
4. Returns both prediction (0/1) and probability (0.0-1.0)

## 🐛 Troubleshooting

**Error: "Model file not found"**
```bash
# Train the model first
cd ../phishing_detector
python train_baseline.py --input ../Phishing_Email.csv
```

**Error: "Module not found"**
```bash
pip install -r requirements.txt
```

**Messages not updating**
- Check browser console (F12)
- Verify server is running
- Try manual refresh button

**Database locked**
- Close other connections to chat.db
- Delete chat.db and restart app

## 🚀 Usage Example

1. **Open app** → Automatic username assigned
2. **Change username** → Click "👤 Change Username"
3. **Send message** → Type and press Enter or click Send
4. **Phishing test** → Try: "Click here to verify your account: http://suspicious-link.com"
5. **View stats** → See detection rate at top
6. **Clear chat** → Click "🗑️ Clear Chat"

## 📈 Enhancement Ideas

Want to improve it? Try adding:
- User authentication
- Message editing/deletion
- File attachments
- Message reactions
- User profiles
- Dark mode
- Export chat history
- Admin dashboard
- API for external apps

## 🎉 Demo Messages

Try these to test phishing detection:

**Safe Messages:**
```
Hello! How are you today?
The meeting is scheduled for 3 PM.
Thanks for your help yesterday!
```

**Phishing Messages:**
```
URGENT! Verify your account now: http://fake-bank.com
You won $1,000,000! Click here immediately!!!
Your password will expire! Reset now: http://phishing.com
```

---

**Made for Master 1 Machine Learning Project**  
Demonstrates practical application of NLP phishing detection model.
