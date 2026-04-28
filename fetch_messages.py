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
    """Convert username or numeric ID to proper format"""
    chat_input = str(chat_input).strip()
    
    # If it's a username (with or without @)
    if chat_input.startswith('@') or not chat_input.lstrip('-').isdigit():
        # Remove @ if present
        username = chat_input.lstrip('@')
        return username  # Telethon will handle as username
    else:
        # Numeric ID
        return int(chat_input)

async def main():
    init_db()
    
    if SESSION_STRING:
        from telethon.sessions import StringSession
        client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    else:
        client = TelegramClient('session', API_ID, API_HASH)
    
    await client.start(phone=PHONE)
    
    # Parse chat ID (supports both numeric and username)
    chat_identifier = parse_chat_id(CHAT_ID_INPUT)
    
    try:
        # Get entity (works with both numeric ID and username)
        entity = await client.get_entity(chat_identifier)
        
        # Get chat title
        if hasattr(entity, 'title'):
            chat_title = entity.title
        elif hasattr(entity, 'first_name'):
            chat_title = f"{entity.first_name} {entity.last_name or ''}".strip()
        elif hasattr(entity, 'username'):
            chat_title = f"@{entity.username}"
        else:
            chat_title = str(chat_identifier)
        
        # Save chat info (use numeric ID as primary key)
        numeric_chat_id = entity.id
        save_chat(numeric_chat_id, chat_title)
        
        print(f"Connected to: {chat_title}")
        print(f"Numeric ID: {numeric_chat_id}")
        
        # Get last 100 messages
        messages = await client.get_messages(entity, limit=100)
        
        count = 0
        for msg in messages:
            if msg.text and not isinstance(msg, MessageService):
                sender = await msg.get_sender()
                if sender:
                    sender_name = sender.first_name or sender.username or 'System'
                else:
                    sender_name = 'Unknown'
                
                save_message(
                    chat_id=numeric_chat_id,
                    msg_id=msg.id,
                    sender_name=sender_name,
                    date=str(msg.date),
                    text=msg.text
                )
                count += 1
        
        print(f"Saved {count} text messages")
        
        # Encrypt the database
        if ENCRYPTION_KEY and os.path.exists('messages.db'):
            encrypt_file(ENCRYPTION_KEY, 'messages.db', 'messages.db.encrypted')
            print("Database encrypted to messages.db.encrypted")
            os.remove('messages.db')
            print("Unencrypted database removed")
            
    except Exception as e:
        print(f"Error: {e}")
        print(f"Could not find chat with identifier: {chat_identifier}")
        print("Make sure:")
        print("  - Username exists and is correct")
        print("  - Numeric ID is correct (for groups use -100 prefix)")
        print("  - You are a member of the chat")

if __name__ == '__main__':
    asyncio.run(main())