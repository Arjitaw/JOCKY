import base64
from crypto import encrypt, decrypt

def test_roundtrip():
    message = {
        "action": "hash",
        "target": "file",
        "path": "hello.txt"

    }

    encrypted = encrypt(message)
    decrypted = decrypt(encrypted)

    assert decrypted == message
    print("PASS: roundtrip test passed.")

if __name__ == "__main__":
    test_roundtrip()
    test_wrong_key()
    test_tampered_ciphertext()
    test_wrong_iv()
    test_corrupted_base64()
    test_different_plaintext_different_ciphertext()
    

def test_wrong_key():
    import crypto

    message = {"action": "hash", "target": "file", "path": "hello.txt"}
    encrypted = encrypt(message)

    original_key = crypto.KEY
    crypto.KEY = b"ffffffffffffffffffffffffffffffff"

    try:
        decrypted = decrypt(encrypted)
        print("Decrypted with wrong key (no crash):", decrypted)
    except Exception as e:
        print("PASS: wrong key failed as expected ->", type(e).__name__, e)
    finally:
        crypto.KEY = original_key

def test_tampered_ciphertext():
    message = {"action": "hash", "target": "file", "path": "hello.txt"}
    encrypted = encrypt(message)

    raw = bytearray(base64.b64decode(encrypted))
    raw[20] ^= 0xFF
    tampered = base64.b64encode(bytes(raw)).decode("utf-8")

    try:
        decrypted = decrypt(tampered)
        print("Decrypted tampered ciphertext (no crash!):", decrypted)
    except Exception as e:
        print("PASS: tampered ciphertext failed ->", type(e).__name__, e)

def test_wrong_iv():
    message = {"action": "hash", "target": "file", "path": "hello.txt"}
    encrypted = encrypt(message)

    raw = bytearray(base64.b64decode(encrypted))
    raw[0] ^= 0xFF
    tampered = base64.b64encode(bytes(raw)).decode("utf-8")

    try:
        decrypted = decrypt(tampered)
        print("Decrypted with wrong IV (no crash!):", decrypted)
    except Exception as e:
        print("PASS: wrong IV failed ->", type(e).__name__, e)

def test_corrupted_base64():
    message = {"action": "hash", "target": "file", "path": "hello.txt"}
    encrypted = encrypt(message)

    tampered = encrypted[:-2] + "!!"

    try:
        decrypted = decrypt(tampered)
        print("Decrypted corrupted base64 (no crash!):", decrypted)
    except Exception as e:
        print("PASS: corrupted base64 failed ->", type(e).__name__, e)

def test_different_plaintext_different_ciphertext():
    message1 = {"action": "hash", "target": "file", "path": "hello.txt"}
    message2 = {"action": "hash", "target": "file", "path": "world.txt"}

    encrypted1 = encrypt(message1)
    encrypted2 = encrypt(message2)

    assert encrypted1 != encrypted2
    print("PASS: different plaintexts produce different ciphertexts")
