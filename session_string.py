from telethon import TelegramClient
client = TelegramClient('session', API_ID, API_HASH)
client.start(phone=PHONE)
print(client.session.save())