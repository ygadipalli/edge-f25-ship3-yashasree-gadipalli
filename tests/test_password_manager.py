"""Tests for the password manager track stubs."""

import os
import json
import pytest

import password_manager as pm
from password_manager import (
    hash_password,
    verify_password,
    encrypt_password,
    decrypt_password,
    safe_load,
    safe_save,
    login_user,
)

def test_register_user_exists_and_unimplemented() -> None:
    assert hasattr(pm, "register_user"), "register_user should exist"
    with pytest.raises(NotImplementedError):
        pm.register_user("user", "pass")


def test_add_password_exists_and_unimplemented() -> None:
    assert hasattr(pm, "add_password"), "add_password should exist"
    with pytest.raises(NotImplementedError):
        pm.add_password("example.com", "user", "password123")


def test_get_passwords_exists_and_unimplemented() -> None:
    assert hasattr(pm, "get_passwords"), "get_passwords should exist"
    with pytest.raises(NotImplementedError):
        pm.get_passwords()


# UNIT TESTS

def test_hash_and_verify():
    """Unit test: hashing + verifying passwords"""
    pw = "hello123"
    hashed = hash_password(pw)
    assert verify_password(pw, hashed) is True
    assert verify_password("wrongpw", hashed) is False


def test_encrypt_decrypt_roundtrip():
    """Unit test: encryption and decryption produce original text"""
    key = hash_password("master123")[:32]  # derive a short fake key for test
    text = "mysecret"
    enc = encrypt_password(text, key)
    dec = decrypt_password(enc, key)
    assert dec == text


def test_safe_save_and_load():
    """Unit test: integrity + JSON writing"""
    test_file = "data/test_passwords.json"
    data = {"entries": [{"id": 1, "site": "github.com"}]}
    safe_save(data, filename=test_file)

    loaded = safe_load(filename=test_file)
    assert loaded["entries"][0]["site"] == "github.com"

    # cleanup
    os.remove(test_file)


# INTEGRATION TEST

def test_integration_register_login_and_store_password(tmp_path):
    """
    Golden-path integration test:
    - create a fake user_data file
    - register user
    - login user
    - save passwords
    - load passwords back
    """

    # Step 1: Create fake user storage location
    user_file = tmp_path / "user_data.json"
    passwords_file = tmp_path / "passwords.json"

    # Fake: manually simulate registration
    username = "alice"
    pw = "strongpw"
    hashed = hash_password(pw)

    with open(user_file, "w") as f:
        json.dump({username: hashed}, f)

    # Step 2: confirm login works
    assert login_user(username, pw, user_file=user_file) is True
    assert login_user(username, "wrongpw", user_file=user_file) is False

    # Step 3: save password entries via safe_save
    sample = {"entries": [{"id": 1, "site": "github.com", "username": "alice"}]}
    safe_save(sample, filename=passwords_file)

    # Step 4: load and verify
    loaded = safe_load(filename=passwords_file)
    assert loaded["entries"][0]["site"] == "github.com"
