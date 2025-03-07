from flask import Flask, request, jsonify, render_template_string
import hashlib
import json

app = Flask(__name__)

SECRET_FILE = "secret.json"
TREASURE_FILE = "treasure.txt"

def load_secret_data():
    try:
        with open(SECRET_FILE, "r") as file:
            secret_data = json.load(file)
            return secret_data["key"], secret_data["hash"]
    except FileNotFoundError:
        return None, None

def load_treasure():
    try:
        with open(TREASURE_FILE, "r") as file:
            return file.read()
    except FileNotFoundError:
        return None

def transform_passkey(passkey, key):
    return "".join(chr(ord(c) ^ (key % 256)) for c in passkey)

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_passkey = request.form.get("passkey")
        transformation_key, stored_hash = load_secret_data()

        if transformation_key is None or stored_hash is None:
            return jsonify({"error": "Secret file not found!"}), 500

        transformed_passkey = transform_passkey(user_passkey, transformation_key)

        if hash_passkey(transformed_passkey) == stored_hash:
            treasure = load_treasure()
            if treasure is None:
                return jsonify({"error": "Treasure file not found!"}), 500
            return jsonify({"message": "Access Granted!", "treasure": treasure})

        return jsonify({"error": "Access Denied! Incorrect passkey."}), 403

    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Treasure Unlock</title>
        </head>
        <body>
            <h2>Enter the passkey to unlock the treasure</h2>
            <form method="post">
                <input type="password" name="passkey" required>
                <button type="submit">Unlock</button>
            </form>
        </body>
        </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
