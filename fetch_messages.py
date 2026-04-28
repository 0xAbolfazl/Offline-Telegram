import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import MessageService
from dotenv import load_dotenv
from db import init_db, save_chat, save_message
from crypto_utils import encrypt_file

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')
SESSION_STRING = os.getenv('SESSION_STRING')
CHAT_ID_INPUT = os.getenv('CHAT_ID')
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

def parse_chat_id(chat_input):
    chat_input = str(chat_input).strip()
    if chat_input.startswith('@') or not chat_input.lstrip('-').isdigit():
        return chat_input.lstrip('@')
    else:
        return int(chat_input)

async def main():
    init_db()
    
    if SESSION_STRING:
        from telethon.sessions import StringSession
        client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    else:
        client = TelegramClient('session', API_ID, API_HASH)
    
    await client.start(phone=PHONE)
    
    # Get my user ID and name
    me = await client.get_me()
    my_id = me.id
    my_username = me.username
    print(f"Logged in as: {me.first_name} (ID: {my_id})")
    
    chat_identifier = parse_chat_id(CHAT_ID_INPUT)
    
    try:
        entity = await client.get_entity(chat_identifier)
        
        if hasattr(entity, 'title'):
            chat_title = entity.title
        elif hasattr(entity, 'first_name'):
            chat_title = f"{entity.first_name} {entity.last_name or ''}".strip()
        elif hasattr(entity, 'username'):
            chat_title = f"@{entity.username}"
        else:
            chat_title = str(chat_identifier)
        
        numeric_chat_id = entity.id
        save_chat(numeric_chat_id, chat_title)
        print(f"Connected to chat: {chat_title}")
        
        messages = await client.get_messages(entity, limit=100)
        count = 0
        
        for msg in messages:
            if msg.text and not isinstance(msg, MessageService):
                sender = await msg.get_sender()
                if sender:
                    sender_name = sender.first_name or sender.username or 'System'
                    sender_id = sender.id
                    is_self = (sender_id == my_id)   # Crucial line
                else:
                    sender_name = 'Unknown'
                    sender_id = 0
                    is_self = False
                
                save_message(
                    chat_id=numeric_chat_id,
                    msg_id=msg.id,
                    sender_name=sender_name,
                    sender_id=sender_id,
                    is_self=1 if is_self else 0,
                    date=str(msg.date),
                    text=msg.text
                )
                count += 1
        
        print(f"Saved {count} text messages")
        
        if ENCRYPTION_KEY and os.path.exists('messages.db'):
            encrypt_file(ENCRYPTION_KEY, 'messages.db', 'messages.db.encrypted')
            print("Database encrypted to messages.db.encrypted")
            os.remove('messages.db')
            print("Unencrypted database removed")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    asyncio.run(main())