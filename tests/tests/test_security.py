import os
import json
import pytest
from password_manager import add_password, get_passwords, register_user

def test_add_and_retrieve_encrypted_password(tmp_path):
    # setup fake user
    register_user("testuser", "master123")
    
    # add a password
    add_password("example.com", "user1", "secret123")
    
    # load raw data file
    with open("data/passwords.json", "r") as f:
        data = json.load(f)
    
    # check stored password is not plaintext
    for entry in data["entries"]:
        assert entry["password"] != "secret123"
    
    # check get_passwords returns data
    retrieved = get_passwords()
    assert len(retrieved["entries"]) > 0
