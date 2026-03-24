from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open("secret.key","wb") as f:
    f.write(key)

cipher = Fernet(key)

with open("data.txt","rb") as f:
    file = f.read()

encrypted = cipher.encrypt(file)

with open("encrypted.enc","wb") as f:
    f.write(encrypted)

print("File encrypted successfully")