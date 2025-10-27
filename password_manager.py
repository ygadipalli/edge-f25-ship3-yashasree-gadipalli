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
import shutil

def create_backup():
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
    os.makedirs("data", exist_ok=True)
    if os.path.exists(DATA_FILE):
        data["version"] = data.get("version", 1)
        shutil.copy(DATA_FILE, BACKUP_FILE)
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        json.dump(data, tmp, indent=2)
        temp_name = tmp.name
    os.replace(temp_name, DATA_FILE)

def register_user(username: str, master_password: str) -> None:
    hashed = hashlib.sha256(master_password.encode()).hexdigest()
    if os.path.exists("data/user_data.json"):
        with open("data/user_data.json", "r") as f:
            users = json.load(f)
    else:
        users = {}    
    users[username] = hashed
    os.makedirs("data", exist_ok=True)
    with open("data/user_data.json", "w") as f:
        json.dump(users, f)
    """Register a new user with a master password.

    You will hash and store the master password in a
    JSON file for authentication.  This stub does nothing.

    Args:
        username: The username for the account.
        master_password: The master password to use.
    """

def add_password(site: str, username: str, password: str, notes="", tags=None) -> None:
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    tags = tags or []
    if not site or not username or not password:
        print("All fields are required.")
        return
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {"version": 1, "entries": []}

    for e in data["entries"]:
        if e["site"] == site and e["username"] == username:
            print("A password for this site and username already exists.")
            choice = input("Do you want to (S)kip, (O)verwrite, or (K)eep both? ").strip().lower()
            if choice == "s":
                print("Skipped.")
                return
            elif choice == "o":
                e["password"] = password
                e["last_updated"] = datetime.now().isoformat()
                safe_save(data)
                print("Password overwritten.")
                return
            elif choice == "k":
                # allow a duplicate entry to be added
                break
            else:
                print("Invalid choice. Skipped.")
                return

    new_id = len(data["entries"]) + 1
    entry = {
        "id": new_id,
        "site": site,
        "username": username,
        "password": password,
        "notes": notes,
        "tags": tags,
        "last_updated": datetime.now().isoformat()
    }
    data["entries"].append(entry)
    safe_save(data)
    """Store a password for a given site.

    You will encrypt the password and save it to a JSON file,
    associating it with the site and username.  This stub does nothing.

    Args:
        site: The website or service name.
        username: The account username for the site.
        password: The password to store.
    """

def get_passwords() -> dict:
    if not os.path.exists(DATA_FILE):
        return {"version": 1, "entries": []}
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: failed to read data file ({e}). Creating a fresh structure. Your backup may contain previous data.")
        # try to restore from backup if exists
        if os.path.exists(BACKUP_FILE):
            try:
                with open(BACKUP_FILE, "r") as bf:
                    data = json.load(bf)
                    print("Loaded data from backup.")
            except Exception:
                data = {"version": 1, "entries": []}
        else:
            data = {"version": 1, "entries": []}
    # If old format (list), convert it
    if isinstance(data, list):
        data = {"version": 1, "entries": data}
    return data

    """Retrieve all stored passwords.

    This will read from an encrypted JSON file and return a list
    of dictionaries containing site, username and password.  For now
    it raises `NotImplementedError`.

    Returns:
        A list of stored passwords.
    """

def main() -> None:
    """Entry point for the password manager.

    When run directly, this prints a greeting.  You will replace this
    with registration, login and menu functionality in future ships.
    """
    print("Welcome to the Password Manager!")

    def login_user(username: str, master_passwords: str) -> bool:
        if not os.path.exists("data/user_data.json"):
            print("No users registered. Please register first.")
            return False
        with open("data/user_data.json", "r") as f:
            users = json.load(f)
        hashed = hashlib.sha256(master_password.encode()).hexdigest()
        return users.get(username) == hashed

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
        if choice == "2":
            username = input("Enter username: ")
            master_password = input("Enter master password: ")
            register_user(username, master_password)
            print("User registered.")
        elif choice == "1":
            username = input("Enter username: ")
            master_password = input("Enter master password: ")
            if not login_user(username, master_password):
                print("Login failed.")
                return
            print("Login successful.")      
            logged_in = True
            current_user = username      
        elif choice == "3":
            if not logged_in:
                print("Please log in first.")
                continue
            site = input("Enter site: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            add_password(site, username, password)
            print("Password added.")
        elif choice == "4":
            if not logged_in:
                print("Please log in first.")
                continue
            data = get_passwords()
            if not data["entries"]:
                print("No passwords stored.")
                continue
            for e in data["entries"]:
                masked_pw = "*" * min(8, len(e.get("password", "")))  # show a consistent mask
                print(f"{e['id']}. {e['site']} | {e['username']} | Password: {masked_pw} | Last updated: {e.get('last_updated')}")
            reveal = input("Reveal a password? Enter ID or press Enter to skip: ").strip()
            if reveal:
                if not reveal.isdigit():
                    print("Invalid ID.")
                else:
                    for e in data["entries"]:
                        if str(e["id"]) == reveal:
                            print(f"Password for {e['site']} ({e['username']}): {e['password']}")
                            break
                    else:
                        print("ID not found.")
        elif choice == "5":
            if not logged_in:
                print("Please log in first.")
                continue
            site = input("Enter site name to search: ").strip()
            data = get_passwords()
            found = False
            # iterate through the entries list inside the data dict
            for entry in data.get("entries", []):
                if entry.get("site", "").lower() == site.lower():
                    # mask password when showing search results
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
            for e in data["entries"]:
                if str(e["id"]) == entry_id:
                    new_pw = input("Enter new password: ")
                    e["password"] = new_pw
                    e["last_updated"] = datetime.now().isoformat()
                    safe_save(data)
                    print("Password updated.")
                    break
            else:
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
            # confirm exists
            match = next((e for e in data["entries"] if str(e["id"]) == entry_id), None)
            if not match:
                print("ID not found.")
                continue
            confirm = input(f"Are you sure you want to delete '{match['site']}' for user '{match['username']}'? (y/n): ").strip().lower()
            if confirm != "y":
                print("Delete cancelled.")
                continue
            # perform delete
            new_entries = [e for e in data["entries"] if str(e["id"]) != entry_id]
            data["entries"] = new_entries
            safe_save(data)
            print("Password deleted.")
        elif choice == "7.5": #optional hidden option
            create_backup()
        elif choice == "8":
            print("Goodbye! All data saved safely.")
            break

if __name__ == "__main__":
    main()