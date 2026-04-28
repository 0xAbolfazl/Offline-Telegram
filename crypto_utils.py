import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_file(key_base64, input_file, output_file):
    """Decrypt an encrypted file"""
    if not os.path.exists(input_file):
        return False
    
    key = base64.b64decode(key_base64)
    
    with open(input_file, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    with open(output_file, 'wb') as f:
        f.write(plaintext)
    
    return True

def encrypt_file(key_base64, input_file, output_file):
    """Encrypt a file"""
    key = base64.b64decode(key_base64)
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)
    
    return True

def ensure_db_decrypted(encryption_key):
    """Check if decrypted db exists, if not try to decrypt from encrypted file"""
    if os.path.exists('messages.db'):
        return True
    
    if os.path.exists('messages.db.encrypted') and encryption_key:
        print("Decrypting database...")
        success = decrypt_file(encryption_key, 'messages.db.encrypted', 'messages.db')
        if success:
            print("Database decrypted successfully")
            return True
        else:
            print("Failed to decrypt database")
            return False
    
    print("No database file found")
    return False