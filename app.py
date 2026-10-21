from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet
import os
import threading
import webbrowser

app = Flask(__name__)

STORAGE = "storage"

# Create storage folder
if not os.path.exists(STORAGE):
    os.makedirs(STORAGE)


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")


# ---------------- UPLOAD & ENCRYPT ----------------
@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']

    if file.filename == "":
        return "❌ No file selected"

    filepath = os.path.join(STORAGE, file.filename)
    file.save(filepath)

    # Save filename
    with open(os.path.join(STORAGE, "filename.txt"), "w") as f:
        f.write(file.filename)

    # Read file
    with open(filepath, "rb") as f:
        data = f.read()

    # Detect sensitive content
    try:
        text = data.decode('utf-8').lower()
    except:
        text = ""

    keywords = ["password", "bank", "account", "confidential", "salary"]
    is_sensitive = any(word in text for word in keywords)

    with open(os.path.join(STORAGE, "sensitive.txt"), "w") as f:
        f.write("yes" if is_sensitive else "no")

    # Save password if sensitive
    user_password = request.form.get("password")

    if is_sensitive:
        if not user_password:
            return "❌ Sensitive file requires password"
        with open(os.path.join(STORAGE, "user_password.txt"), "w") as f:
            f.write(user_password)

    # Encrypt file
    key = Fernet.generate_key()
    with open(os.path.join(STORAGE, "secret.key"), "wb") as f:
        f.write(key)

    cipher = Fernet(key)
    encrypted = cipher.encrypt(data)

    with open(os.path.join(STORAGE, "encrypted.enc"), "wb") as f:
        f.write(encrypted)

    return "✅ File encrypted successfully"


# ---------------- VIEW ENCRYPTED ----------------
@app.route('/view_encrypted')
def view_encrypted():

    path = os.path.join(STORAGE, "encrypted.enc")

    if not os.path.exists(path):
        return "❌ No encrypted file found"

    with open(path, "rb") as f:
        data = f.read()

    return "<h3>🔒 Encrypted Data</h3><pre>" + data.decode(errors='ignore') + "</pre>"


# ---------------- DOWNLOAD ENCRYPTED ----------------
@app.route('/download_encrypted')
def download_encrypted():

    enc_path = os.path.join(STORAGE, "encrypted.enc")
    key_path = os.path.join(STORAGE, "secret.key")

    if not os.path.exists(enc_path):
        return "❌ No encrypted file"

    # IMPORTANT: Tell user to download BOTH
    return f"""
    <h3>Download both files:</h3>
    <a href="/get_enc">Download Encrypted File</a><br><br>
    <a href="/get_key">Download Key File</a>
    """


@app.route('/get_enc')
def get_enc():
    return send_file(os.path.join(STORAGE, "encrypted.enc"), as_attachment=True)


@app.route('/get_key')
def get_key():
    return send_file(os.path.join(STORAGE, "secret.key"), as_attachment=True)


# ---------------- UPLOAD ENCRYPTED + KEY ----------------
@app.route('/upload_encrypted', methods=['POST'])
def upload_encrypted():

    enc_file = request.files['encfile']
    key_file = request.files['keyfile']

    if enc_file.filename == "" or key_file.filename == "":
        return "❌ Select both encrypted file and key"

    enc_path = os.path.join(STORAGE, "uploaded.enc")
    key_path = os.path.join(STORAGE, "secret.key")

    enc_file.save(enc_path)
    key_file.save(key_path)

    return "✅ Encrypted file + key uploaded"


# ---------------- DECRYPT ----------------
@app.route('/decrypt_uploaded', methods=['POST'])
def decrypt_uploaded():

    password = request.form.get("password")

    sensitive_flag = open(os.path.join(STORAGE, "sensitive.txt")).read()

    if sensitive_flag == "yes":
        saved_password = open(os.path.join(STORAGE, "user_password.txt")).read()

        if password != saved_password:
            return "❌ Wrong Password"

    key = open(os.path.join(STORAGE, "secret.key"), "rb").read()
    cipher = Fernet(key)

    with open(os.path.join(STORAGE, "uploaded.enc"), "rb") as f:
        encrypted = f.read()

    decrypted = cipher.decrypt(encrypted)

    filename = open(os.path.join(STORAGE, "filename.txt")).read()
    output_file = os.path.join(STORAGE, "decrypted_" + filename)

    with open(output_file, "wb") as f:
        f.write(decrypted)

    return send_file(output_file, as_attachment=True)


# ---------------- AUTO OPEN ----------------
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


# ---------------- RUN ----------------
if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)