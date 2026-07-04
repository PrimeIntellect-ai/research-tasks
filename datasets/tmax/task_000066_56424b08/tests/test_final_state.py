# test_final_state.py

import os
import json
import pytest

def get_expected_lines():
    app_path = '/home/user/webapp/app.py'
    if not os.path.exists(app_path):
        return 15, 23 # Fallback to known truth if file is missing/modified beyond recognition

    open_redirect_line = None
    sqli_line = None

    with open(app_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "return redirect(" in line:
            open_redirect_line = i + 1
        if "cursor.execute(" in line and "query" in line and "+" in line:
            sqli_line = i + 1

    return open_redirect_line or 15, sqli_line or 23

def get_expected_token():
    tokens_path = '/home/user/webapp/tokens.txt'
    if not os.path.exists(tokens_path):
        return 61966 # Fallback

    with open(tokens_path, 'r') as f:
        tokens = [int(line.strip()) for line in f if line.strip().isdigit()]

    if len(tokens) < 3:
        return 61966

    x0, x1, x2 = tokens[0], tokens[1], tokens[2]
    m = 65537

    # a * (x1 - x0) = (x2 - x1) mod m
    diff_x1_x0 = (x1 - x0) % m
    diff_x2_x1 = (x2 - x1) % m

    try:
        inv = pow(diff_x1_x0, -1, m)
        a = (diff_x2_x1 * inv) % m
        c = (x1 - a * x0) % m
        x3 = (a * x2 + c) % m
        return x3
    except ValueError:
        return 61966

def test_audit_report_exists():
    report_path = '/home/user/audit_report.json'
    assert os.path.isfile(report_path), f"The audit report file {report_path} was not found."

def test_audit_report_content():
    report_path = '/home/user/audit_report.json'
    assert os.path.isfile(report_path), "Missing audit report."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/audit_report.json does not contain valid JSON.")

    expected_redirect, expected_sqli = get_expected_lines()
    expected_token = get_expected_token()

    assert "open_redirect_line" in data, "Key 'open_redirect_line' is missing from the JSON report."
    assert "sqli_line" in data, "Key 'sqli_line' is missing from the JSON report."
    assert "next_predicted_token" in data, "Key 'next_predicted_token' is missing from the JSON report."

    assert data["open_redirect_line"] == expected_redirect, f"Expected open_redirect_line to be {expected_redirect}, got {data['open_redirect_line']}."
    assert data["sqli_line"] == expected_sqli, f"Expected sqli_line to be {expected_sqli}, got {data['sqli_line']}."
    assert data["next_predicted_token"] == expected_token, f"Expected next_predicted_token to be {expected_token}, got {data['next_predicted_token']}."