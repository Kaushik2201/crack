import hashlib
import json

SECRET_FILE = "secret.json"
TREASURE_FILE = "treasure.txt"

def load_secret_data():
    try:
        with open(SECRET_FILE, "r") as file:
            secret_data = json.load(file)
            return secret_data["key"], secret_data["hash"]
    except FileNotFoundError:
        print("❌ Error: Secret file not found!")
        exit(1)

def load_treasure():
    try:
        with open(TREASURE_FILE, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("❌ Error: Treasure file not found!")
        exit(1)

def transform_passkey(passkey, key):
    modified_passkey = "".join(chr(ord(c) ^ (key % 256)) for c in passkey)
    return modified_passkey

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def main():
    transformation_key, stored_hash = load_secret_data()
    user_passkey = input("Enter the passkey to unlock the treasure: ")

    transformed_passkey = transform_passkey(user_passkey, transformation_key)
    
    if hash_passkey(transformed_passkey) == stored_hash:
        print("✅ Access Granted! Here is your treasure:\n")
        print(load_treasure())
    else:
        print("❌ Access Denied! Incorrect passkey.")

if __name__ == "__main__":
    main()
