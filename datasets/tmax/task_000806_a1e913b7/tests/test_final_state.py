# test_final_state.py
import os
import json
import base64
import pytest

def b64url_encode(data: bytes) -> str:
    """Base64Url encode with no padding."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def b64url_decode(b64_str: str) -> bytes:
    """Base64Url decode with automatic padding."""
    pad_len = 4 - (len(b64_str) % 4)
    pad_len = 0 if pad_len == 4 else pad_len
    padded = b64_str + ('=' * pad_len)
    return base64.urlsafe_b64decode(padded)

@pytest.fixture
def expected_data():
    input_file = "/home/user/tokens.txt"
    assert os.path.isfile(input_file), f"Input file {input_file} is missing."

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_results = []
    for line in lines:
        parts = line.split('.')
        assert len(parts) == 3, f"Invalid JWT format in input file: {line}"

        header_b64, payload_b64, _ = parts

        # Decode original payload
        payload_bytes = b64url_decode(payload_b64)
        original_payload = json.loads(payload_bytes)

        username = original_payload.get("username", "")

        # Redact original payload
        redacted_payload = dict(original_payload)
        if "credit_card" in redacted_payload:
            redacted_payload["credit_card"] = "REDACTED"

        # Forge token
        forged_header = {"alg": "none"}
        forged_payload = dict(original_payload)
        if "role" in forged_payload:
            forged_payload["role"] = "admin"

        forged_header_b64 = b64url_encode(json.dumps(forged_header, separators=(',', ':')).encode('utf-8'))
        forged_payload_b64 = b64url_encode(json.dumps(forged_payload, separators=(',', ':')).encode('utf-8'))

        forged_token = f"{forged_header_b64}.{forged_payload_b64}."

        expected_results.append({
            "username": username,
            "forged_token": forged_token,
            "redacted_original_payload": redacted_payload
        })

    return expected_results

def test_output_file_exists():
    """Verify that the pwned_tokens.json file was created."""
    output_file = "/home/user/pwned_tokens.json"
    assert os.path.isfile(output_file), f"Output file {output_file} was not found."

def test_output_file_valid_json():
    """Verify that the output file is valid JSON."""
    output_file = "/home/user/pwned_tokens.json"
    if not os.path.isfile(output_file):
        pytest.skip("Output file missing")

    with open(output_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file is not valid JSON: {e}")

    assert isinstance(data, list), "Output JSON must be an array of objects."

def test_output_data_correctness(expected_data):
    """Verify that the output JSON matches the expected forged and redacted data."""
    output_file = "/home/user/pwned_tokens.json"
    if not os.path.isfile(output_file):
        pytest.skip("Output file missing")

    with open(output_file, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Output file is not valid JSON")

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} items in output, found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert isinstance(actual, dict), f"Item {i} in output array is not a JSON object."

        # Check username
        assert "username" in actual, f"Item {i} is missing 'username' field."
        assert actual["username"] == expected["username"], f"Item {i} username mismatch. Expected '{expected['username']}', got '{actual['username']}'."

        # Check forged token
        assert "forged_token" in actual, f"Item {i} is missing 'forged_token' field."
        assert actual["forged_token"] == expected["forged_token"], f"Item {i} forged_token mismatch."

        # Check redacted payload
        assert "redacted_original_payload" in actual, f"Item {i} is missing 'redacted_original_payload' field."

        # The task specifies redacted_original_payload is a string containing JSON, but JSON parsers 
        # might parse it differently depending on how the student wrote it. If the student outputted a JSON string:
        actual_redacted = actual["redacted_original_payload"]
        if isinstance(actual_redacted, str):
            try:
                actual_redacted_parsed = json.loads(actual_redacted)
            except json.JSONDecodeError:
                pytest.fail(f"Item {i} 'redacted_original_payload' is a string but not valid JSON.")
        else:
            # If they embedded it as a JSON object directly
            actual_redacted_parsed = actual_redacted

        assert actual_redacted_parsed == expected["redacted_original_payload"], f"Item {i} redacted_original_payload mismatch. Expected {expected['redacted_original_payload']}, got {actual_redacted_parsed}."