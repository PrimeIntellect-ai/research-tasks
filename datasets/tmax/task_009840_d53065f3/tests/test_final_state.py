# test_final_state.py

import os
import json
import stat
import pytest

def test_firewall_policy_log():
    log_path = '/home/user/firewall_policy.log'
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = {
        "BLOCK /home/user/intercepted/payload_01.dat",
        "ALLOW /home/user/intercepted/payload_02.dat",
        "BLOCK /home/user/intercepted/payload_03.dat"
    }

    actual_lines = set(lines)
    assert actual_lines == expected_lines, f"Firewall policy log contents are incorrect. Expected {expected_lines}, got {actual_lines}"

def test_safe_token_file():
    token_path = '/home/user/safe_token.txt'
    assert os.path.isfile(token_path), f"Token file {token_path} is missing."

    # Check contents
    with open(token_path, 'r') as f:
        content = f.read().strip()

    assert content == "X9f2M4pL1vQ8z", f"Token file contains incorrect value. Expected 'X9f2M4pL1vQ8z', got '{content}'"

    # Check permissions (0400)
    st = os.stat(token_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o400, f"Token file permissions are incorrect. Expected 0o400, got {oct(permissions)}"

def test_final_report_json():
    report_path = '/home/user/final_report.json'
    assert os.path.isfile(report_path), f"Final report {report_path} is missing."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Final report {report_path} is not valid JSON.")

    expected_data = {
        "scanned_files": 3,
        "blocked_files": 2,
        "allowed_files": 1,
        "extracted_token": "X9f2M4pL1vQ8z"
    }

    assert data == expected_data, f"Final report JSON contents are incorrect. Expected {expected_data}, got {data}"