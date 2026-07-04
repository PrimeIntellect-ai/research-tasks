# test_final_state.py

import os
import json
import stat

def test_clean_traffic_permissions_and_existence():
    """Test that clean_traffic.json exists and has 0600 permissions."""
    file_path = "/home/user/clean_traffic.json"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    st = os.stat(file_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o600, f"Permissions of {file_path} are {oct(permissions)}, expected 0o600."

def test_clean_traffic_contents():
    """Test that clean_traffic.json has correctly redacted headers."""
    file_path = "/home/user/clean_traffic.json"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{file_path} does not contain valid JSON."

    assert len(data) == 4, f"Expected 4 records in {file_path}, got {len(data)}."

    # Record 0
    assert data[0]["ip"] == "192.168.1.50"
    assert data[0]["headers"].get("Authorization") == "[REDACTED]", "Authorization header not redacted in record 0."
    assert data[0]["headers"].get("Set-Cookie") == "[REDACTED]", "Set-Cookie missing 'Secure' not redacted in record 0."

    # Record 1
    assert data[1]["ip"] == "10.0.0.5"
    assert data[1]["headers"].get("Set-Cookie") == "track_id=xyz987; Secure; HttpOnly", "Valid Set-Cookie was incorrectly modified in record 1."

    # Record 2
    assert data[2]["ip"] == "172.16.0.10"
    assert data[2]["headers"].get("Set-Cookie") == "[REDACTED]", "Set-Cookie missing both directives not redacted in record 2."

    # Record 3
    assert data[3]["ip"] == "192.168.1.50"
    assert data[3]["headers"].get("Authorization") == "[REDACTED]", "Authorization header not redacted in record 3."
    assert data[3]["headers"].get("Set-Cookie") == "[REDACTED]", "Set-Cookie missing 'HttpOnly' not redacted in record 3."

def test_blocked_ips_contents():
    """Test that blocked_ips.txt contains the correct sorted unique IPs."""
    file_path = "/home/user/blocked_ips.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        ips = [line.strip() for line in f if line.strip()]

    expected_ips = ["172.16.0.10", "192.168.1.50"]
    assert ips == expected_ips, f"Blocked IPs incorrect. Expected {expected_ips}, got {ips}."