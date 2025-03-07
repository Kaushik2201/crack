from flask import Flask, request, jsonify
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
        return {"error": "❌ Error: Secret file not found!"}

def load_treasure():
    try:
        with open(TREASURE_FILE, "r") as file:
            return file.read()
    except FileNotFoundError:
        return {"error": "❌ Error: Treasure file not found!"}

def transform_passkey(passkey, key):
    return "".join(chr(ord(c) ^ (key % 256)) for c in passkey)

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

@app.route('/unlock', methods=['POST'])
def unlock_treasure():
    data = request.json
    user_passkey = data.get("passkey", "")

    transformation_key, stored_hash = load_secret_data()
    transformed_passkey = transform_passkey(user_passkey, transformation_key)

    if hash_passkey(transformed_passkey) == stored_hash:
        return jsonify({"message": "✅ Access Granted!", "treasure": load_treasure()})
    else:
        return jsonify({"error": "❌ Access Denied! Incorrect passkey."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
