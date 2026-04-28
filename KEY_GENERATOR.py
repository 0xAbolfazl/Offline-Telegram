import secrets
import base64

key = secrets.token_bytes(32)
key_base64 = base64.b64encode(key).decode()
print(f"Your encryption key: {key_base64}")