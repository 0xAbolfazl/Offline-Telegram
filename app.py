from flask import Flask, render_template
from db import init_db, get_all_chats, get_messages, get_my_name, get_chat_title
from crypto_utils import ensure_db_decrypted
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

def prepare_database():
    if os.path.exists('dbs/messages.db.encrypted'):
        shutil.copy('dbs/messages.db.encrypted', 'messages.db.encrypted')
        print("Copied encrypted database from dbs/ folder")
    
    if ENCRYPTION_KEY:
        if ensure_db_decrypted(ENCRYPTION_KEY):
            init_db()
            print("Database ready")
            return True
    else:
        print("Warning: ENCRYPTION_KEY not set in .env")
    return False

@app.route('/')
def index():
    chats = get_all_chats()
    return render_template('index.html', chats=chats)

@app.route('/chat/<int:chat_id>')
def view_chat(chat_id):
    messages = get_messages(chat_id, limit=200)
    my_name = get_my_name()
    chat_title = get_chat_title(chat_id)
    return render_template('chat.html', messages=messages, my_name=my_name, chat_id=chat_id, chat_title=chat_title)

if __name__ == '__main__':
    prepare_database()
    app.run(debug=True, port=5000)