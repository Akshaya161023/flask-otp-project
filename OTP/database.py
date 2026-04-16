import json, os

DB_FILE = "users.json"

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

def register_user(name, email):
    users = load_users()
    if email in users:
        return False, "Email already registered"
    users[email] = {"name": name, "email": email}
    save_users(users)
    return True, "Registered successfully"

def user_exists(email):
    users = load_users()
    return email in users

def get_user(email):
    users = load_users()
    return users.get(email)