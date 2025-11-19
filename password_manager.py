"""Simple password manager (stub).

This module provides placeholder functions for a command‑line password
manager.  Eventually it will allow users to register with a master
password, store encrypted passwords for various sites and retrieve them.
For now, it contains stubs that raise `NotImplementedError` and prints
a greeting when executed.
"""

import json
import os
import hashlib
import shutil
import tempfile
from datetime import datetime
from cryptography.fernet import Fernet
from hashlib import pbkdf2_hmac
import base64

# Global variable to store the active encryption key
active_key = None

# -----------------------
# Input validation helpers
# -----------------------
UNSAFE_CHARS = set("{}[]\\<>")  # characters we disallow in site/username

def sanitize_field(s: str) -> str:
    """Trim whitespace and normalize internal spacing."""
    return s.strip()

def has_unsafe_chars(s: str) -> bool:
    """Return True if any disallowed character is present."""
    return any(c in UNSAFE_CHARS for c in s)

def validate_nonempty(s: str, name: str) -> bool:
    """Ensure field is not empty after trimming. Prints friendly error."""
    if s is None:
        print(f"{name} is required.")
        return False
    s2 = s.strip()
    if s2 == "":
        print(f"{name} cannot be empty or whitespace.")
        return False
    return True

def validate_site_username(site: str, username: str) -> bool:
    """Validate site and username fields: non-empty and no unsafe characters."""
    site = sanitize_field(site)
    username = sanitize_field(username)
    if not validate_nonempty(site, "Site"):
        return False
    if not validate_nonempty(username, "Username"):
        return False
    if has_unsafe_chars(site):
        print("Site contains unsafe characters ({} [] \\ < >).")
        return False
    if has_unsafe_chars(username):
        print("Username contains unsafe characters ({} [] \\ < >).")
        return False
    return True

def validate_password(password: str) -> bool:
    """Ensure password is not empty and has a modest minimum length."""
    if not validate_nonempty(password, "Password"):
        return False
    if len(password.strip()) < 4:
        print("Password must be at least 4 characters long.")
        return False
    return True

def hash_password(password: str) -> str:
    """Hash a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def derive_key(master_password: str) -> bytes:
    """Derive an encryption key from the master password."""
    salt = b'ship6_fixed_salt'  # in a real app, store this safely or generate per-user
    key = pbkdf2_hmac(
        "sha256",
        master_password.encode(),
        salt,
        100000
    )
    return base64.urlsafe_b64encode(key)

def encrypt_password(password: str, key: bytes) -> str:
    """Encrypt a password using Fernet encryption."""
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt_password(token: str, key: bytes) -> str:
    """Decrypt a password using Fernet encryption."""
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()

def save_hash(data_file: str) -> None:
    """Save a hash of the data file for integrity checking."""
    if os.path.exists(data_file):
        with open(data_file, "rb") as f:
            content = f.read()
        hash_value = hashlib.sha256(content).hexdigest()
        os.makedirs("data", exist_ok=True)
        with open("data/hash.txt", "w") as h:
            h.write(hash_value)

def verify_hash(data_file: str) -> bool:
    """Verify the hash of the data file matches the stored hash."""
    if not os.path.exists("data/hash.txt"):
        return True  # no hash saved yet
    with open("data/hash.txt") as h:
        expected = h.read().strip()
    with open(data_file, "rb") as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    return actual == expected

def create_backup():
    """Create a timestamped backup of the passwords file."""
    os.makedirs("backups", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backups/passwords_{timestamp}.json"
    if os.path.exists("data/passwords.json"):
        shutil.copy("data/passwords.json", backup_name)
        print(f"Backup created: {backup_name}")
    else:
        print("No data to back up.")

DATA_FILE = "data/passwords.json"
BACKUP_FILE = "data/passwords.bak"

def safe_save(data):
    """Safely save data to the passwords file with backup."""
    os.makedirs("data", exist_ok=True)
    if os.path.exists(DATA_FILE):
        data["version"] = data.get("version", 1)
        shutil.copy(DATA_FILE, BACKUP_FILE)
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        json.dump(data, tmp, indent=2)
        temp_name = tmp.name
    os.replace(temp_name, DATA_FILE)
    save_hash(DATA_FILE)

def register_user(username: str, master_password: str) -> None:
    """Register a new user with a hashed master password after validating input."""
    username = sanitize_field(username)
    if not validate_nonempty(username, "Username"):
        return
    if has_unsafe_chars(username):
        print("Username contains unsafe characters and cannot be used.")
        return
    if not validate_password(master_password):
        return

    hashed = hash_password(master_password)

    os.makedirs("data", exist_ok=True)
    user_file = "data/user_data.json"
    if os.path.exists(user_file):
        try:
            with open(user_file, "r") as f:
                users = json.load(f)
        except Exception:
            users = {}
    else:
        users = {}

    if username in users:
        print("That username is already registered.")
        return

    users[username] = hashed
    with open(user_file, "w") as f:
        json.dump(users, f)
    print(f"User '{username}' registered.")

def add_password(site: str, username: str, password: str, notes="", tags=None) -> None:
    """Store a password for a given site."""
    global active_key
    if active_key is None:
        print("No active encryption key. Login first.")
        return
    
    tags = tags or []
    site = sanitize_field(site)
    username = sanitize_field(username)

    if not validate_site_username(site, username):
        return
    if not validate_password(password):
        return

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            print("Warning: data file unreadable — starting fresh structure.")
            data = {"version": 1, "entries": []}
    else:
        data = {"version": 1, "entries": []}

    # duplicate check on normalized fields
    for e in data["entries"]:
        if e.get("site") == site and e.get("username") == username:
            print("A password for this site and username already exists.")
            choice = input("Do you want to (S)kip, (O)verwrite, or (K)eep both? ").strip().lower()
            if choice == "s":
                print("Skipped.")
                return
            elif choice == "o":
                e["password"] = encrypt_password(password, active_key)
                e["last_updated"] = datetime.now().isoformat()
                safe_save(data)
                print("Password overwritten.")
                return
            elif choice == "k":
                break
            else:
                print("Invalid choice. Skipped.")
                return

    new_id = len(data["entries"]) + 1
    entry = {
        "id": new_id,
        "site": site,
        "username": username,
        "password": encrypt_password(password, active_key),
        "notes": notes,
        "tags": tags,
        "last_updated": datetime.now().isoformat()
    }
    data["entries"].append(entry)
    safe_save(data)
    print("Password added.")

def get_passwords() -> dict:
    """Retrieve all stored passwords."""
    if not os.path.exists(DATA_FILE):
        return {"version": 1, "entries": []}
    try:
        if not verify_hash(DATA_FILE):
            print("⚠️ Warning: passwords.json may have been modified outside the app.")
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: failed to read data file ({e}). Creating a fresh structure.")
        if os.path.exists(BACKUP_FILE):
            try:
                with open(BACKUP_FILE, "r") as bf:
                    data = json.load(bf)
                    print("Loaded data from backup.")
            except Exception:
                data = {"version": 1, "entries": []}
        else:
            data = {"version": 1, "entries": []}
    
    if isinstance(data, list):
        data = {"version": 1, "entries": data}
    return data

def login_user(username: str, master_password: str) -> bool:
    """Authenticate a user and set the active encryption key."""
    global active_key
    if not os.path.exists("data/user_data.json"):
        print("No users registered. Please register first.")
        return False
    try:
        with open("data/user_data.json", "r") as f:
            users = json.load(f)
    except Exception:
        print("Could not read user data. Please register again or check your files.")
        return False
    
    hashed = hash_password(master_password)
    if users.get(username) == hashed:
        active_key = derive_key(master_password)
        return True
    print("Invalid username or password.")
    return False

def main() -> None:
    """Entry point for the password manager."""
    print("Welcome to the Password Manager!")

    logged_in = False
    current_user = None
    
    while True:
        print("\nOptions:")
        print("1. Login")
        print("2. Register")
        print("3. Add password")
        print("4. View passwords")
        print("5. Search passwords")
        print("6. Edit password")
        print("7. Delete password")
        print("8. Quit")
        choice = input("Choose an option: ")
        
        while choice not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("Invalid option. Please enter 1, 2, 3, 4, 5, 6, 7 or 8.")
            choice = input("Choose an option: ")
        
        if choice == "1":
            username = input("Enter username: ")
            master_password = input("Enter master password: ")
            if login_user(username, master_password):
                print("Login successful.")
                logged_in = True
                current_user = username
            else:
                print("Login failed.")
        
        elif choice == "2":
            username = input("Enter a username: ").strip()
            if not username:
                print("Username cannot be empty.")
                continue
            master_password = input("Enter a master password: ").strip()
            if not master_password:
                print("Master password cannot be empty.")
                continue
            register_user(username, master_password)
        
        elif choice == "3":
            if not logged_in:
                print("Please log in first.")
                continue
            site = input("Enter site: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            add_password(site, username, password)
        
        elif choice == "4":
            if not logged_in:
                print("Please log in first.")
                continue
            data = get_passwords()
            if not data["entries"]:
                print("No passwords stored.")
                continue
            for e in data["entries"]:
                masked_pw = "*" * 8
                print(f"{e['id']}. {e['site']} | {e['username']} | Password: {masked_pw} | Last updated: {e.get('last_updated')}")
            reveal = input("Reveal a password? Enter ID or press Enter to skip: ").strip()
            if reveal:
                if not reveal.isdigit():
                    print("Invalid ID.")
                else:
                    found = False
                    for e in data["entries"]:
                        if str(e["id"]) == reveal:
                            decrypted_pw = decrypt_password(e["password"], active_key)
                            print(f"Password for {e['site']} ({e['username']}): {decrypted_pw}")
                            found = True
                            break
                    if not found:
                        print("ID not found.")
        
        elif choice == "5":
            if not logged_in:
                print("Please log in first.")
                continue
            site = input("Enter site name to search: ").strip()
            data = get_passwords()
            found = False
            for entry in data.get("entries", []):
                if entry.get("site", "").lower() == site.lower():
                    masked = "*" * 8
                    print(f"ID {entry['id']}: {entry['site']} | {entry['username']} | password: {masked} | Last updated: {entry.get('last_updated')}")
                    found = True
            if not found:
                print("No passwords found for that site.")
        
        elif choice == "6":
            if not logged_in:
                print("Please log in first.")
                continue
            data = get_passwords()
            if not data["entries"]:
                print("No passwords stored.")
                continue
            for e in data["entries"]:
                print(f"{e['id']}: {e['site']} ({e['username']})")
            entry_id = input("Enter ID to edit: ").strip()
            if not entry_id.isdigit():
                print("Invalid ID. Please enter a number.")
                continue
            found = False
            for e in data["entries"]:
                if str(e["id"]) == entry_id:
                    new_pw = input("Enter new password: ")
                    e["password"] = encrypt_password(new_pw, active_key)
                    e["last_updated"] = datetime.now().isoformat()
                    safe_save(data)
                    print("Password updated.")
                    found = True
                    break
            if not found:
                print("ID not found.")
        
        elif choice == "7":
            if not logged_in:
                print("Please log in first.")
                continue
            data = get_passwords()
            if not data["entries"]:
                print("No passwords stored.")
                continue
            for e in data["entries"]:
                print(f"{e['id']}: {e['site']} ({e['username']})")
            entry_id = input("Enter ID to delete: ").strip()
            if not entry_id.isdigit():
                print("Invalid ID. Please enter a number.")
                continue
            match = next((e for e in data["entries"] if str(e["id"]) == entry_id), None)
            if not match:
                print("ID not found.")
                continue
            confirm = input(f"Are you sure you want to delete '{match['site']}' for user '{match['username']}'? (y/n): ").strip().lower()
            if confirm != "y":
                print("Delete cancelled.")
                continue
            new_entries = [e for e in data["entries"] if str(e["id"]) != entry_id]
            data["entries"] = new_entries
            safe_save(data)
            print("Password deleted.")
        
        elif choice == "8":
            print("Goodbye! All data saved safely.")
            break

if __name__ == "__main__":
    main()
