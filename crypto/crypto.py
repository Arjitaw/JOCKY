import base64
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7


KEY = b"0123456789abcdef0123456789abcdef"


def encrypt_file(file_path):
    """
    Reads a file, encrypts its contents using AES-CBC,
    and writes the encrypted data back to the file.

    The IV is stored at the beginning of the encrypted file.
    """

    with open(file_path, "rb") as file:
        plaintext = file.read()

    iv = os.urandom(16)

    padder = PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(
        algorithms.AES(KEY),
        modes.CBC(iv)
    )

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    with open(file_path, "wb") as file:
        file.write(iv + ciphertext)

    return {
        "action": "encrypt",
        "path": file_path,
        "status": "success",
        "message": "File encrypted successfully"
    }


def decrypt_file(file_path):
    """
    Reads an encrypted file, extracts the IV,
    decrypts the contents, and restores the original file data.
    """

    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    cipher = Cipher(
        algorithms.AES(KEY),
        modes.CBC(iv)
    )

    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = PKCS7(128).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()

    with open(file_path, "wb") as file:
        file.write(plaintext)

    return {
        "action": "decrypt",
        "path": file_path,
        "status": "success",
        "message": "File decrypted successfully"
    }