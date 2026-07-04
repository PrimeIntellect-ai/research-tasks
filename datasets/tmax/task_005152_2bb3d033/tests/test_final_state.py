# test_final_state.py

import os
import json
import re
import pytest

try:
    from cryptography.fernet import Fernet
except ImportError:
    Fernet = None

def test_safe_audit_log_exists():
    assert os.path.exists("/home/user/safe_audit.log"), "/home/user/safe_audit.log does not exist"
    assert os.path.isfile("/home/user/safe_audit.log"), "/home/user/safe_audit.log is not a file"

def test_bandit_report_exists_and_valid():
    report_path = "/home/user/bandit_report.json"
    assert os.path.exists(report_path), f"{report_path} does not exist"
    assert os.path.isfile(report_path), f"{report_path} is not a file"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not valid JSON")

    assert "results" in data or "metrics" in data, "JSON does not look like a bandit report"

def test_safe_audit_log_content():
    if Fernet is None:
        pytest.fail("cryptography library is required for this test but not installed.")

    key_path = "/home/user/fernet.key"
    assert os.path.exists(key_path), "Fernet key file is missing"

    with open(key_path, "rb") as f:
        key = f.read().strip()

    f = Fernet(key)

    safe_log_path = "/home/user/safe_audit.log"
    assert os.path.exists(safe_log_path), "safe_audit.log is missing"

    with open(safe_log_path, "r") as file:
        content = file.read()

    # Extract all ENC(...) tokens
    tokens = re.findall(r"ENC\(([^)]+)\)", content)
    assert len(tokens) == 2, f"Expected exactly 2 encrypted tokens in the log, found {len(tokens)}"

    decrypted_values = []
    for token in tokens:
        try:
            decrypted = f.decrypt(token.encode('utf-8')).decode('utf-8')
            decrypted_values.append(decrypted)
        except Exception as e:
            pytest.fail(f"Failed to decrypt token '{token[:10]}...': {e}")

    assert "1234567812345678" in decrypted_values, "First credit card number was not encrypted properly"
    assert "9876543210987654" in decrypted_values, "Second credit card number was not encrypted properly"

    # Verify the rest of the log lines match the original format
    raw_log_path = "/home/user/raw_audit.log"
    with open(raw_log_path, "r") as file:
        raw_content = file.read()

    # Replace the 16-digit numbers in raw_content with a regex pattern and match against safe_content
    # Since the tokens are long, we can just replace the ENC(...) in safe_content with the decrypted values
    # and compare to raw_content.
    restored_content = content
    for token, decrypted in zip(tokens, decrypted_values):
        restored_content = restored_content.replace(f"ENC({token})", decrypted)

    assert restored_content == raw_content, "The rest of the log lines do not match the original format"