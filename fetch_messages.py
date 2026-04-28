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
CHAT_IDS_INPUT = os.getenv('CHAT_IDS')   
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
    
    me = await client.get_me()
    my_id = me.id
    print(f"Logged in as: {me.first_name} (ID: {my_id})")
    
    chat_ids_list = [cid.strip() for cid in CHAT_IDS_INPUT.split(',')]
    
    for chat_identifier_str in chat_ids_list:
        chat_identifier = parse_chat_id(chat_identifier_str)
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
            print(f"\nConnected to: {chat_title}")
            
            messages = await client.get_messages(entity, limit=100)
            count = 0
            for msg in messages:
                if msg.text and not isinstance(msg, MessageService):
                    sender = await msg.get_sender()
                    if sender:
                        sender_name = sender.first_name or sender.username or 'System'
                        sender_id = sender.id
                        is_self = (sender_id == my_id)
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
        except Exception as e:
            print(f"Error with {chat_identifier_str}: {e}")
    
    if ENCRYPTION_KEY and os.path.exists('messages.db'):
        encrypt_file(ENCRYPTION_KEY, 'messages.db', 'messages.db.encrypted')
        print("\nDatabase encrypted successfully")
        os.remove('messages.db')

if __name__ == '__main__':
    asyncio.run(main())