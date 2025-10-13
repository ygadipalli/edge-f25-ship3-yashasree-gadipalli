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

def add_password(site: str, username: str, password: str) -> None:
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    if os.path.exists("data/passwords.json"):
        with open("data/passwords.json", "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append({"site": site, "username": username, "password": hashed_pw})
    with open("data/passwords.json", "w") as f:
        json.dump(data, f)

    """Store a password for a given site.

    You will encrypt the password and save it to a JSON file,
    associating it with the site and username.  This stub does nothing.

    Args:
        site: The website or service name.
        username: The account username for the site.
        password: The password to store.
    """

def get_passwords() -> list[dict]:
    if os.path.exists("data/passwords.json"):
        with open("data/passwords.json", "r") as f:
            data = json.load(f)
        return data
    else:
        return []
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
        print("6. Quit")
        choice = input("Choose an option: ")
        while choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Invalid option. Please enter 1, 2, 3, 4, 5, or 6.")
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
            passwords = get_passwords()
            for entry in passwords:
                print(entry)
        elif choice == "5":
            if not logged_in:
                print("Please log in first.")
                continue
            site = input("Enter site name to search: ")
            passwords = get_passwords()
            found = False
            for entry in passwords:
                if entry["site"].lower() == site.lower():
                    print(entry)
                    found = True
            if not found:
                print("No passwords found for that site.")
        elif choice == "6":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()