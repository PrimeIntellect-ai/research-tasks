# test_final_state.py
import os
import json
import base64
import pytest

def get_expected_alerts(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    expected_alerts = []
    for req in data:
        ip = req.get("ip", "")
        path = req.get("path", "")

        # Rule 1: CWE-22
        if "../" in path or "%2E%2E%2F" in path:
            expected_alerts.append(f"{ip} - CWE-22")

        # Rule 2: CWE-269
        headers = req.get("headers", {})
        cookie = headers.get("Cookie", "")
        if "session=" in cookie:
            # Extract session value
            session_val = cookie.split("session=")[1].split(";")[0]
            try:
                decoded = base64.b64decode(session_val).decode('utf-8')
                session_data = json.loads(decoded)
                role = session_data.get("role")
                if role in ["admin", "administrator"]:
                    expected_alerts.append(f"{ip} - CWE-269")
            except Exception:
                pass

    return expected_alerts

def test_alerts_log_exists():
    """Check if the alerts.log file was created."""
    assert os.path.exists("/home/user/alerts.log"), "/home/user/alerts.log does not exist."
    assert os.path.isfile("/home/user/alerts.log"), "/home/user/alerts.log is not a file."

def test_alerts_log_content():
    """Check if the alerts.log contains the correct flagged requests."""
    json_path = "/home/user/http_traffic.json"
    log_path = "/home/user/alerts.log"

    assert os.path.exists(json_path), f"Source file {json_path} is missing."
    assert os.path.exists(log_path), f"Output file {log_path} is missing."

    expected_alerts = get_expected_alerts(json_path)

    with open(log_path, 'r') as f:
        actual_alerts = [line.strip() for line in f if line.strip()]

    assert actual_alerts == expected_alerts, (
        f"Contents of {log_path} do not match the expected output.\n"
        f"Expected: {expected_alerts}\n"
        f"Actual: {actual_alerts}"
    )

def test_script_exists():
    """Check if the script was created."""
    assert os.path.exists("/home/user/detect_attacks.py"), "/home/user/detect_attacks.py does not exist."
    assert os.path.isfile("/home/user/detect_attacks.py"), "/home/user/detect_attacks.py is not a file."