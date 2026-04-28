import sqlite3
import os

DB_PATH = 'messages.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                chat_id INTEGER PRIMARY KEY,
                title TEXT,
                last_fetch TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                message_id INTEGER,
                sender_name TEXT,
                date TEXT,
                text TEXT,
                UNIQUE(chat_id, message_id)
            )
        ''')
        conn.commit()

def save_chat(chat_id, title):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT OR REPLACE INTO chats (chat_id, title, last_fetch)
            VALUES (?, ?, datetime('now'))
        ''', (chat_id, title))

def save_message(chat_id, msg_id, sender_name, date, text):
    with sqlite3.connect(DB_PATH) as conn:
        try:
            conn.execute('''
                INSERT INTO messages (chat_id, message_id, sender_name, date, text)
                VALUES (?, ?, ?, ?, ?)
            ''', (chat_id, msg_id, sender_name, date, text))
            conn.commit()
        except sqlite3.IntegrityError:
            pass

def get_all_chats():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute('SELECT chat_id, title FROM chats ORDER BY last_fetch DESC')
        return cur.fetchall()

def get_messages(chat_id, limit=100):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute('''
            SELECT sender_name, date, text FROM messages
            WHERE chat_id = ?
            ORDER BY date DESC LIMIT ?
        ''', (chat_id, limit))
        return cur.fetchall()[::-1]  # oldest first