# test_final_state.py
import os
import json

def test_audit_trail_log_exists_and_correct():
    log_path = "/home/user/audit_trail.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. The audit trail log was not generated."

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, f"Expected at least 2 lines in {log_path}, found {len(lines)}."

    line1 = lines[0].strip()
    line2 = lines[1].strip()

    assert line1 == "5192", f"Line 1 of {log_path} is incorrect. Expected '5192', got '{line1}'."

    expected_json = {"status": "success", "token": "COMPLIANCE_TOKEN_A8F92C"}
    try:
        actual_json = json.loads(line2)
    except json.JSONDecodeError:
        assert False, f"Line 2 of {log_path} is not valid JSON. Got: '{line2}'"

    assert actual_json == expected_json, f"Line 2 JSON is incorrect. Expected {expected_json}, got {actual_json}."

def test_cracker_go_exists():
    path = "/home/user/cracker.go"
    assert os.path.isfile(path), f"File {path} does not exist. The Go cracker program is missing."

def test_secure_audit_sh_exists():
    path = "/home/user/secure_audit.sh"
    assert os.path.isfile(path), f"File {path} does not exist. The bash script is missing."