# test_final_state.py
import os
import stat
import json
import subprocess
import requests
from requests.auth import HTTPBasicAuth

def test_recovered_creds_file():
    path = "/app/recovered_creds.json"
    assert os.path.isfile(path), f"File missing: {path}"

    # Check permissions (0600)
    st = os.stat(path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Incorrect permissions on {path}: expected 0600, got {oct(perms)}"

    # Check contents
    with open(path, "r") as f:
        try:
            creds = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{path} is not valid JSON"

    expected_creds = {
        "admin": "hunter2",
        "db_user": "secret",
        "backup_svc": "apple"
    }

    assert creds == expected_creds, f"Contents of {path} do not match the expected recovered credentials."

def get_legacy_token(username, password):
    result = subprocess.run(
        ["/app/legacy_token_gen", username, password],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def test_http_service_behavior():
    base_url = "http://127.0.0.1:8000"

    # 1. GET /verify with Basic Auth admin:hunter2 -> 200
    try:
        resp = requests.get(f"{base_url}/verify", auth=HTTPBasicAuth("admin", "hunter2"), timeout=2)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to HTTP service at {base_url}: {e}"
    assert resp.status_code == 200, f"Expected 200 OK for valid basic auth, got {resp.status_code}. Response: {resp.text}"

    # 2. GET /verify with Basic Auth admin:wrong -> 401
    resp = requests.get(f"{base_url}/verify", auth=HTTPBasicAuth("admin", "wrong"), timeout=2)
    assert resp.status_code == 401, f"Expected 401 Unauthorized for invalid basic auth, got {resp.status_code}. Response: {resp.text}"

    # 3. Call legacy_token_gen
    admin_token = get_legacy_token("admin", "hunter2")

    # 4. POST /rotate with valid token
    rotate_payload = {"username": "admin", "new_password": "NewSecurePassword1!"}
    headers = {"X-Legacy-Token": admin_token}
    resp = requests.post(f"{base_url}/rotate", json=rotate_payload, headers=headers, timeout=2)
    assert resp.status_code == 200, f"Expected 200 OK for valid rotation, got {resp.status_code}. Response: {resp.text}"

    # 5. GET /verify with old password -> 401
    resp = requests.get(f"{base_url}/verify", auth=HTTPBasicAuth("admin", "hunter2"), timeout=2)
    assert resp.status_code == 401, f"Expected 401 Unauthorized for old password after rotation, got {resp.status_code}. Response: {resp.text}"

    # 6. GET /verify with new password -> 200
    resp = requests.get(f"{base_url}/verify", auth=HTTPBasicAuth("admin", "NewSecurePassword1!"), timeout=2)
    assert resp.status_code == 200, f"Expected 200 OK for new password after rotation, got {resp.status_code}. Response: {resp.text}"

    # 7. POST /rotate with invalid token -> 401
    rotate_payload_invalid = {"username": "db_user", "new_password": "Hacked"}
    headers_invalid = {"X-Legacy-Token": "invalidtoken"}
    resp = requests.post(f"{base_url}/rotate", json=rotate_payload_invalid, headers=headers_invalid, timeout=2)
    assert resp.status_code == 401, f"Expected 401 Unauthorized for invalid token rotation, got {resp.status_code}. Response: {resp.text}"