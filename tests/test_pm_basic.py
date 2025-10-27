import json
from pathlib import Path
import pytest
from datetime import datetime
import password_manager as pm

def test_add_and_get(tmp_path, monkeypatch):
    mf = tmp_path / "passwords.json"
    monkeypatch.setattr("password_manager.DATA_FILE", str(mf))
    data = {"version": 1, "entries": []}
    pm.safe_save(data)
    pm.add_password("siteA", "userA", "pwA")
    res = pm.get_passwords()
    assert len(res["entries"]) == 1
    assert res["entries"][0]["site"] == "siteA"

def test_delete(tmp_path, monkeypatch):
    mf = tmp_path / "passwords.json"
    monkeypatch.setattr("password_manager.DATA_FILE", str(mf))
    data = {"version": 1, "entries": [
        {"id": 1, "site": "x", "username": "y", "password": "z", "last_updated": datetime.now().isoformat()}
    ]}
    pm.safe_save(data)
    d = pm.get_passwords()
    d["entries"] = []
    pm.safe_save(d)
    assert pm.get_passwords()["entries"] == []
