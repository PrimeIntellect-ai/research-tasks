# test_final_state.py
import os
import json
import urllib.parse
import pytest

def test_audit_report_exists_and_correct():
    path = "/home/user/audit_report.json"
    assert os.path.exists(path), f"Expected file {path} is missing."
    assert os.path.isfile(path), f"Expected {path} to be a file."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "cwe_id" in data, "Key 'cwe_id' is missing in audit_report.json."
    assert data["cwe_id"] == "CWE-601", f"Expected cwe_id to be 'CWE-601', got '{data['cwe_id']}'."

    assert "cracked_password" in data, "Key 'cracked_password' is missing in audit_report.json."
    assert data["cracked_password"] == "s3cr3t_p4ss!", f"Expected cracked_password to be 's3cr3t_p4ss!', got '{data['cracked_password']}'."

    assert "exploit_payload" in data, "Key 'exploit_payload' is missing in audit_report.json."
    payload = data["exploit_payload"]
    decoded_payload = urllib.parse.unquote(payload)
    assert decoded_payload == "http://malicious.example.com/login", f"Expected exploit_payload to decode to 'http://malicious.example.com/login', got '{decoded_payload}'."

def test_verify_script_exists_and_executable():
    path = "/home/user/verify.sh"
    assert os.path.exists(path), f"Expected file {path} is missing."
    assert os.path.isfile(path), f"Expected {path} to be a file."
    assert os.access(path, os.X_OK), f"Expected {path} to be executable."

def test_exploit_result_exists_and_correct():
    path = "/home/user/exploit_result.txt"
    assert os.path.exists(path), f"Expected file {path} is missing."
    assert os.path.isfile(path), f"Expected {path} to be a file."

    with open(path, 'r') as f:
        content = f.read()

    assert "HTTP/1.1 302 Found" in content, "Expected 'HTTP/1.1 302 Found' in exploit_result.txt."
    assert "Location: http://malicious.example.com/login" in content, "Expected 'Location: http://malicious.example.com/login' in exploit_result.txt."