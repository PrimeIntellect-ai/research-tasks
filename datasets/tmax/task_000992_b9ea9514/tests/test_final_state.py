# test_final_state.py
import os
import json

def test_updater_c_exists():
    path = "/home/user/updater.c"
    assert os.path.isfile(path), f"The C source file {path} does not exist."

def test_updater_binary_exists():
    path = "/home/user/updater"
    assert os.path.isfile(path), f"The compiled binary {path} does not exist."
    assert os.access(path, os.X_OK), f"The file {path} is not executable."

def test_policy_patched():
    path = "/home/user/policy.conf"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read()

    assert "AllowPort 80" in content, "policy.conf is missing 'AllowPort 80'"
    assert "AllowPort 443" in content, "policy.conf is missing 'AllowPort 443' (patch not applied correctly)"
    assert "AdminUser admin" in content, "policy.conf is missing 'AdminUser admin' (patch not applied correctly)"
    assert "AdminUser root" not in content, "policy.conf still contains 'AdminUser root' (patch not applied correctly)"

def test_audit_log_json():
    path = "/home/user/audit_log.json"
    assert os.path.isfile(path), f"The file {path} does not exist. Did the C program run and send the WebSocket message?"

    with open(path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0 and lines[0] != "", f"The {path} file is empty."

    # Parse the last line as JSON
    try:
        data = json.loads(lines[-1])
    except json.JSONDecodeError:
        assert False, f"The last line of {path} is not valid JSON."

    assert data.get("status") == "patched", f"Expected status 'patched', got {data.get('status')}"
    assert data.get("old_checksum") == 44864, f"Expected old_checksum 44864, got {data.get('old_checksum')}"
    assert data.get("new_checksum") == 36816, f"Expected new_checksum 36816, got {data.get('new_checksum')}"