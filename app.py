from flask import Flask, render_template
from db import init_db, get_all_chats, get_messages
from crypto_utils import ensure_db_decrypted
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

if ENCRYPTION_KEY:
    if ensure_db_decrypted(ENCRYPTION_KEY):
        init_db()
        print("Database ready")
    else:
        print("Warning: Could not load database")
else:
    print("Warning: ENCRYPTION_KEY not set, trying to use existing messages.db")
    init_db()

@app.route('/')
def index():
    chats = get_all_chats()
    return render_template('index.html', chats=chats)

@app.route('/chat/<int:chat_id>')
def view_chat(chat_id):
    messages = get_messages(chat_id, limit=200)
    return render_template('chat.html', messages=messages, chat_id=chat_id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)