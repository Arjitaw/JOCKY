import base64
import json
import os
import cryptography.hazmat.primitives.ciphers

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7


KEY = b"0123456789abcdef0123456789abcdef"  
#FOR LATER USE
#KEY = os.urandom(32)  #generates random key


def encrypt(data):
    plaintext = json.dumps(data).encode("utf-8")

    iv =  os.urandom(16)

    padder = PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv))

    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(padded) + encryptor.finalize()

    return base64.b64encode(iv + ciphertext).decode("utf-8")


def decrypt(encrypted_data):
    raw = base64.b64decode(encrypted_data)
    iv = raw[:16]
    ciphertext = raw[16:]

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = PKCS7(128).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()

    return json.loads(plaintext.decode("utf-8"))