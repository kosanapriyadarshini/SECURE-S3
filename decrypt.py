from cryptography.fernet import Fernet
import os

# Path of encrypted file
encrypted_path = os.path.join("storage", "encrypted.enc")

# Read secret key
with open("secret.key", "rb") as f:
    key = f.read()

cipher = Fernet(key)

# Read encrypted data
with open(encrypted_path, "rb") as f:
    encrypted_data = f.read()

# Decrypt data
decrypted_data = cipher.decrypt(encrypted_data)

# Save decrypted file
with open("original_file", "wb") as f:
    f.write(decrypted_data)

print("File decrypted successfully. Check 'original_file'")