# test_final_state.py

import os
import json
import pytest

def test_decrypted_logs():
    """Verify that the encrypted logs were correctly decrypted."""
    decrypted_path = "/home/user/decrypted_logs.txt"

    assert os.path.exists(decrypted_path), f"File not found: {decrypted_path}"

    expected_plaintext = (
        "[INFO] 2024-01-01 Service started\n"
        "[WARN] 2024-01-02 Low memory\n"
        "[INFO] 2024-01-03 Audit log initialized\n"
        "[ERROR] 2024-01-04 Failed login attempt\n"
    )

    with open(decrypted_path, 'r', encoding='utf-8') as f:
        actual_plaintext = f.read()

    assert actual_plaintext == expected_plaintext, (
        f"Contents of {decrypted_path} do not match the expected decrypted plaintext. "
        "Ensure the XOR decryption and Base64 decoding were applied correctly."
    )

def test_vulnerability_proof():
    """Verify that the hidden endpoint was successfully accessed."""
    proof_path = "/home/user/vulnerability_proof.txt"

    assert os.path.exists(proof_path), f"File not found: {proof_path}"

    expected_proof = "VULNERABILITY_CONFIRMED_SYSTEM_COMPROMISED"

    with open(proof_path, 'r', encoding='utf-8') as f:
        actual_proof = f.read().strip()

    assert actual_proof == expected_proof, (
        f"Contents of {proof_path} do not match the expected vulnerability proof. "
        f"Expected '{expected_proof}', but got '{actual_proof}'."
    )

def test_compliance_report():
    """Verify the final compliance report JSON structure and values."""
    report_path = "/home/user/compliance_report.json"

    assert os.path.exists(report_path), f"File not found: {report_path}"

    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse {report_path} as valid JSON: {e}")

    expected_key = "C0mpl1@nc3_K3y_2024"
    expected_endpoint = "/admin_backdoor_v99_debug"
    expected_lines = 4

    assert "encryption_key" in report_data, f"Missing 'encryption_key' in {report_path}"
    assert report_data["encryption_key"] == expected_key, (
        f"Incorrect 'encryption_key'. Expected '{expected_key}', got '{report_data['encryption_key']}'"
    )

    assert "hidden_endpoint" in report_data, f"Missing 'hidden_endpoint' in {report_path}"
    assert report_data["hidden_endpoint"] == expected_endpoint, (
        f"Incorrect 'hidden_endpoint'. Expected '{expected_endpoint}', got '{report_data['hidden_endpoint']}'"
    )

    assert "decrypted_lines" in report_data, f"Missing 'decrypted_lines' in {report_path}"
    assert isinstance(report_data["decrypted_lines"], int), "'decrypted_lines' must be an integer"
    assert report_data["decrypted_lines"] == expected_lines, (
        f"Incorrect 'decrypted_lines'. Expected {expected_lines}, got {report_data['decrypted_lines']}"
    )