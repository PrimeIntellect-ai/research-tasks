# test_final_state.py

import os
import re
import json
import hashlib
import pytest

def test_vulnerable_files_log():
    log_path = "/home/user/vulnerable_files.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist. Did you run the permission audit?"
    assert os.path.isfile(log_path), f"Path {log_path} is not a regular file."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1, f"Expected exactly one entry in {log_path}, but found {len(lines)}."

    line = lines[0]
    # Regex to match: <absolute_file_path> <sha256_hash>
    match = re.match(r'^(/home/user/secure_service/certs/trust\.pem)\s+([a-f0-9]{64})$', line)
    assert match is not None, f"Line in {log_path} is incorrectly formatted or points to the wrong file. Found: {line}"

def test_payload_json():
    payload_path = "/home/user/payload.json"
    assert os.path.exists(payload_path), f"File {payload_path} does not exist. Did you create the payload?"
    assert os.path.isfile(payload_path), f"Path {payload_path} is not a regular file."

    with open(payload_path, 'r') as f:
        try:
            payload = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {payload_path} does not contain valid JSON.")

    assert isinstance(payload, dict), f"JSON root in {payload_path} must be an object/dictionary."
    assert "code" in payload, f"'code' key missing from {payload_path}."
    assert "signature" in payload, f"'signature' key missing from {payload_path}."

    assert isinstance(payload["code"], str), "'code' must be a string."
    assert isinstance(payload["signature"], str), "'signature' must be a string."

def test_final_output_txt():
    output_path = "/home/user/final_output.txt"
    assert os.path.exists(output_path), f"File {output_path} does not exist. Did you execute the service?"
    assert os.path.isfile(output_path), f"Path {output_path} is not a regular file."

    # Compute expected hash dynamically to ensure truth alignment
    expected_hash = hashlib.sha256(b"Pwned_By_Auditor").hexdigest()
    expected_string = f"EXPLOIT_SUCCESS: {expected_hash}"

    with open(output_path, 'r') as f:
        content = f.read()

    assert expected_string in content, f"Expected string '{expected_string}' not found in {output_path}. Execution may have failed or payload was incorrect."