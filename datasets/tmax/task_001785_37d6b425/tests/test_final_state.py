# test_final_state.py

import os
import json
import hashlib

def test_process_audit_exists():
    path = "/home/user/process_audit.py"
    assert os.path.isfile(path), f"Script {path} does not exist."

def test_redacted_report_content_and_format():
    report_path = "/home/user/redacted_report.json"
    assert os.path.isfile(report_path), f"Redacted report {report_path} does not exist."

    with open(report_path, 'r') as f:
        content = f.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        assert False, f"{report_path} is not valid JSON."

    # Validate structure and redaction
    assert "audit_id" in data, "Missing 'audit_id' in redacted report."
    assert "users" in data, "Missing 'users' in redacted report."

    for user in data["users"]:
        assert user.get("password") == "***", "Password was not properly redacted."
        assert user.get("ssn") == "***", "SSN was not properly redacted."
        assert user.get("username") in ["alice", "bob"], "Unexpected username found."

    # Validate formatting (indent=4, sort_keys=True)
    expected_content = json.dumps(data, indent=4, sort_keys=True)
    assert content == expected_content, f"{report_path} is not formatted exactly with indent=4 and sort_keys=True."

def test_report_hash_content():
    report_path = "/home/user/redacted_report.json"
    hash_path = "/home/user/report_hash.txt"

    assert os.path.isfile(report_path), f"Redacted report {report_path} does not exist."
    assert os.path.isfile(hash_path), f"Hash file {hash_path} does not exist."

    with open(report_path, 'rb') as f:
        file_bytes = f.read()

    expected_hash = hashlib.sha256(file_bytes).hexdigest()

    with open(hash_path, 'r') as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Hash in {hash_path} ({actual_hash}) does not match the actual SHA-256 hash of {report_path} ({expected_hash})."