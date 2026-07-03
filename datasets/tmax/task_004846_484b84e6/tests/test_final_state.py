# test_final_state.py
import os
import json
import hashlib

def test_extractor_go_exists():
    path = "/home/user/extractor.go"
    assert os.path.isfile(path), f"File {path} is missing. Did you write the Go program?"

def test_verification_log_exists():
    path = "/home/user/verification_log.json"
    assert os.path.isfile(path), f"File {path} is missing. Did you execute the Go program?"

def test_verification_log_contents():
    path = "/home/user/verification_log.json"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} does not contain valid JSON."

    assert "extracted_policy" in data, f"Key 'extracted_policy' missing in {path}."
    assert "sha256" in data, f"Key 'sha256' missing in {path}."

    policy = data["extracted_policy"]
    assert isinstance(policy, dict), "'extracted_policy' must be a JSON object, not a string."

    assert policy.get("env") == "production", f"Expected policy 'env' to be 'production', got {policy.get('env')}"
    assert policy.get("version") == "1.2.3", f"Expected policy 'version' to be '1.2.3', got {policy.get('version')}"
    assert policy.get("signed") is True, f"Expected policy 'signed' to be True, got {policy.get('signed')}"

    expected_payload = '{"env":"production","version":"1.2.3","signed":true}'
    expected_hash = hashlib.sha256(expected_payload.encode('utf-8')).hexdigest()

    assert data["sha256"] == expected_hash, f"Expected sha256 to be '{expected_hash}', got '{data['sha256']}'"