# test_final_state.py

import os
import json
import pytest

def test_c2_ip_extracted():
    """Verify that the C2 IP address was correctly extracted from the firewall dump."""
    ip_file_path = "/home/user/c2_ip.txt"
    assert os.path.isfile(ip_file_path), f"Expected file {ip_file_path} is missing. Did you save the C2 IP?"

    with open(ip_file_path, "r") as f:
        ip_address = f.read().strip()

    assert ip_address == "192.168.100.45", f"Incorrect C2 IP extracted. Expected '192.168.100.45', but got '{ip_address}'."

def test_payload_zip_decrypted():
    """Verify that the payload was correctly XOR-decrypted and saved as a ZIP file."""
    zip_file_path = "/home/user/forensics/payload.zip"
    assert os.path.isfile(zip_file_path), f"Expected file {zip_file_path} is missing. Did the Go program decrypt the payload?"

    with open(zip_file_path, "rb") as f:
        magic_bytes = f.read(4)

    assert magic_bytes == b"PK\x03\x04", "The decrypted payload.zip does not start with the standard ZIP magic bytes (PK\\x03\\x04). The XOR decryption might be incorrect."

def test_exfiltrated_json_extracted():
    """Verify that the ZIP file was cracked and its contents extracted."""
    json_file_path = "/home/user/forensics/exfiltrated.json"
    assert os.path.isfile(json_file_path), f"Expected file {json_file_path} is missing. Did you crack the ZIP password and extract it?"

def test_evidence_clean_json_redacted():
    """Verify that the sensitive data was properly redacted and saved as valid JSON."""
    clean_file_path = "/home/user/evidence_clean.json"
    assert os.path.isfile(clean_file_path), f"Expected file {clean_file_path} is missing. Did you run the redaction program?"

    with open(clean_file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {clean_file_path} does not contain valid JSON.")

    assert isinstance(data, list), "The redacted JSON data should be an array (list) of objects."
    assert len(data) == 2, f"Expected 2 records in the JSON array, but found {len(data)}."

    expected_usernames = {"admin", "jsmith"}
    found_usernames = set()

    for i, record in enumerate(data):
        assert isinstance(record, dict), f"Record at index {i} is not a JSON object."

        # Check that required fields exist
        for field in ["id", "username", "email", "credit_card"]:
            assert field in record, f"Record at index {i} is missing the '{field}' field."

        # Check redaction
        assert record["credit_card"] == "[REDACTED]", f"The 'credit_card' field for user '{record.get('username')}' was not properly redacted. Expected '[REDACTED]', got '{record['credit_card']}'."

        found_usernames.add(record["username"])

    assert found_usernames == expected_usernames, "The usernames in the redacted JSON do not match the expected original records."