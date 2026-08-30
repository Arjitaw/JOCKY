from pathlib import Path

from crypto.crypto import encrypt_file, decrypt_file


TEST_FILE = Path("test_crypto.txt")


# 1. Create a test file
original_text = "This is a JOCKY crypto test."

TEST_FILE.write_text(original_text, encoding="utf-8")

print("Original file:")
print(TEST_FILE.read_text(encoding="utf-8"))


# 2. Encrypt the file
print("\nEncrypting file...")

result = encrypt_file(str(TEST_FILE))

print(result)


# 3. Check that the file changed
encrypted_data = TEST_FILE.read_bytes()

print("\nEncrypted file size:")
print(len(encrypted_data), "bytes")


# 4. Decrypt the file
print("\nDecrypting file...")

result = decrypt_file(str(TEST_FILE))

print(result)


# 5. Check that the original contents came back
decrypted_text = TEST_FILE.read_text(encoding="utf-8")

print("\nDecrypted file:")
print(decrypted_text)


# 6. Verify automatically
if decrypted_text == original_text:
    print("\n✅ TEST PASSED")
else:
    print("\n❌ TEST FAILED")