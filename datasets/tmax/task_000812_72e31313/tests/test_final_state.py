# test_final_state.py

import os
import re
import requests
import pytest

API_URL = "http://127.0.0.1:9055"
TOKEN = "f9a8b7c6"
HEADERS = {"X-Auth-Token": TOKEN}

def test_cron_file():
    path = "/app/backup.cron"
    assert os.path.isfile(path), f"Cron file {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    # Matches '0 2 * * * /app/backup.sh' with possible extra spaces
    match = re.search(r"^0\s+2\s+\*\s+\*\s+\*\s+/app/backup\.sh", content, re.MULTILINE)
    assert match is not None, f"Cron file {path} does not contain the correct schedule for 2:00 AM."

def test_api_unauthorized():
    try:
        resp = requests.get(f"{API_URL}/api/state?time=2024-01-01T01:00:00")
        assert resp.status_code == 401, f"Expected 401 Unauthorized without token, got {resp.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to API at {API_URL}. Is the server running?")

    try:
        resp = requests.get(f"{API_URL}/api/state?time=2024-01-01T01:00:00", headers={"X-Auth-Token": "wrongtoken"})
        assert resp.status_code == 401, f"Expected 401 Unauthorized with wrong token, got {resp.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to API at {API_URL}. Is the server running?")

def test_api_state_base():
    time_str = "2024-01-01T01:00:00"
    resp = requests.get(f"{API_URL}/api/state?time={time_str}", headers=HEADERS)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

    data = resp.json()
    assert data.get("auth") == {"cpu": 2, "mem": 1024}, f"Incorrect base state for auth: {data.get('auth')}"
    assert data.get("web") == {"cpu": 4, "mem": 2048}, f"Incorrect base state for web: {data.get('web')}"
    assert data.get("db") == {"cpu": 8, "mem": 8192}, f"Incorrect base state for db: {data.get('db')}"

def test_api_state_web_scaled():
    time_str = "2024-01-01T08:30:00"
    resp = requests.get(f"{API_URL}/api/state?time={time_str}", headers=HEADERS)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

    data = resp.json()
    assert data.get("web") == {"cpu": 6, "mem": 4096}, f"Incorrect state for web after scale up: {data.get('web')}"
    assert data.get("db") == {"cpu": 8, "mem": 8192}, f"db state should not have changed yet: {data.get('db')}"

def test_api_state_db_invalid_ignored():
    time_str = "2024-01-01T09:15:00"
    resp = requests.get(f"{API_URL}/api/state?time={time_str}", headers=HEADERS)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

    data = resp.json()
    assert data.get("db") == {"cpu": 8, "mem": 8192}, f"Invalid scale down for db should have been ignored. Got: {data.get('db')}"

def test_api_state_auth_unicode_handled():
    time_str = "2024-01-01T11:00:00"
    resp = requests.get(f"{API_URL}/api/state?time={time_str}", headers=HEADERS)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

    data = resp.json()
    assert data.get("auth") == {"cpu": 4, "mem": 2048}, f"Auth change with bad unicode should have been parsed and applied. Got: {data.get('auth')}"
    assert data.get("web") == {"cpu": 6, "mem": 4096}, f"Web should still be scaled up: {data.get('web')}"
    assert data.get("db") == {"cpu": 8, "mem": 8192}, f"DB should remain at base state: {data.get('db')}"