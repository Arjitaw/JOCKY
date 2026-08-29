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

