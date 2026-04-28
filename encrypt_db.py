import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import hashlib

def encrypt_file(key_base64, input_file, output_file):
    key = base64.b64decode(key_base64)
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)
    
    print(f"Encrypted: {output_file}")

if __name__ == '__main__':
    key = os.environ.get('ENCRYPTION_KEY')
    if not key:
        print("ERROR: ENCRYPTION_KEY not found in secrets")
        exit(1)
    
    if os.path.exists('messages.db'):
        encrypt_file(key, 'messages.db', 'messages.db.encrypted')
        print("Database encrypted successfully")
    else:
        print("No database file found")
        exit(1)