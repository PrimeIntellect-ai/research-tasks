# test_final_state.py

import os
import json
import pytest

def test_audit_trail_exists_and_valid():
    audit_path = "/home/user/audit_trail.json"
    assert os.path.isfile(audit_path), f"File {audit_path} does not exist. The audit trail was not generated."

    with open(audit_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{audit_path} is not valid JSON.")

    # Check decrypted_original_url
    assert "decrypted_original_url" in data, "Key 'decrypted_original_url' missing in audit_trail.json"
    assert data["decrypted_original_url"] == "https://app.local/dashboard", \
        f"Incorrect decrypted_original_url. Expected 'https://app.local/dashboard', got '{data['decrypted_original_url']}'"

    # Check malicious_state_payload
    assert "malicious_state_payload" in data, "Key 'malicious_state_payload' missing in audit_trail.json"
    expected_payload = "2d15fb7e8ec9335a901053073749451da7eb03cda181b53e4c4491c95df949d0dd12dc60b457dc55ce3fbf899321eab07d8b58a129efea110c732a3943dc5a5223ab06e7a27eb84519fbb9fb9d084050"
    assert data["malicious_state_payload"].lower() == expected_payload, \
        f"Incorrect malicious_state_payload. Expected '{expected_payload}', got '{data['malicious_state_payload']}'"

    # Check recommended_csp
    assert "recommended_csp" in data, "Key 'recommended_csp' missing in audit_trail.json"
    csp = data["recommended_csp"].strip()

    # Normalize spaces and semicolons for flexible matching
    csp_normalized = " ".join(csp.replace(";", " ; ").split())

    assert "default-src 'none'" in csp_normalized or "default-src 'none';" in csp.replace(" ", ""), \
        "CSP does not properly set default-src to 'none'."

    assert "script-src 'self' https://apis.local" in csp_normalized or "script-src 'self' https://apis.local;" in csp.replace(" ", "") or "script-src https://apis.local 'self'" in csp_normalized, \
        "CSP does not properly restrict script-src to 'self' and https://apis.local."