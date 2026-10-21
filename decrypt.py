from flask import send_file
import time

@app.route('/decrypt', methods=['POST'])
def decrypt():

    password = request.form.get('password')

    sensitive_flag = open(os.path.join(STORAGE, "sensitive.txt")).read()

    if sensitive_flag == "yes":
        if password != "1234":
            return "❌ Access Denied! Wrong Password"

    key = open(os.path.join(STORAGE, "secret.key"), "rb").read()
    cipher = Fernet(key)

    encrypted_path = os.path.join(STORAGE, "encrypted.enc")

    with open(encrypted_path, "rb") as f:
        encrypted = f.read()

    decrypted = cipher.decrypt(encrypted)

    filename = open(os.path.join(STORAGE, "filename.txt")).read()

    # 🔥 IMPORTANT FIX: absolute path + proper name
    output_file = os.path.abspath(os.path.join(STORAGE, "decrypted_" + filename))

    with open(output_file, "wb") as f:
        f.write(decrypted)

    time.sleep(1)   # ensure file is written

    return send_file(output_file, as_attachment=True)