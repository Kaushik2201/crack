from flask import Flask, render_template, request
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
        return "Treasure file missing!"

def transform_passkey(passkey, key):
    return "".join(chr(ord(c) ^ (key % 256)) for c in passkey)

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        user_passkey = request.form["passkey"]
        transformation_key, stored_hash = load_secret_data()

        if transformation_key is None:
            return "Error: Secret file missing!"

        transformed_passkey = transform_passkey(user_passkey, transformation_key)
        if hash_passkey(transformed_passkey) == stored_hash:
            return render_template("treasure.html", treasure=load_treasure())

        message = "❌ Access Denied! Incorrect passkey."

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
