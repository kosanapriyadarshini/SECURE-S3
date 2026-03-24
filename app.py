from flask import Flask, render_template, request
from cryptography.fernet import Fernet
import os

app = Flask(__name__)

# Create storage folder if it doesn't exist
STORAGE = "storage"
if not os.path.exists(STORAGE):
    os.makedirs(STORAGE)


@app.route('/')
def home():
    return render_template("index.html")


# Upload and encrypt file
@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(STORAGE, file.filename)

    # Save uploaded file
    file.save(filepath)

    # Generate encryption key
    key = Fernet.generate_key()
    with open("secret.key", "wb") as f:
        f.write(key)

    cipher = Fernet(key)

    # Read file
    with open(filepath, "rb") as f:
        data = f.read()

    # Encrypt file
    encrypted = cipher.encrypt(data)

    encrypted_path = os.path.join(STORAGE, "encrypted.enc")

    with open(encrypted_path, "wb") as f:
        f.write(encrypted)

    return "File uploaded and encrypted successfully!"


# Download and decrypt file
@app.route('/download')
def download():

    key = open("secret.key", "rb").read()
    cipher = Fernet(key)

    encrypted_path = os.path.join(STORAGE, "encrypted.enc")

    with open(encrypted_path, "rb") as f:
        encrypted = f.read()

    decrypted = cipher.decrypt(encrypted)

    with open("original_file", "wb") as f:
        f.write(decrypted)

    return "File downloaded and decrypted successfully!"


if __name__ == "__main__":
    app.run(debug=True)