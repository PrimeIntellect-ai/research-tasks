# test_final_state.py
import os
import json
import pytest

def test_cwe_report_exists_and_correct():
    """Verify that the CWE report exists and contains the correct CWE IDs."""
    report_path = "/home/user/cwe_report.txt"
    assert os.path.isfile(report_path), f"CWE report file missing at {report_path}"

    with open(report_path, "r") as f:
        content = f.read().upper()

    # Check for the weak crypto CWE
    assert "CWE-327" in content or "CWE-311" in content, "CWE report is missing the correct CWE ID for weak cryptography (e.g., CWE-327)."

    # Check for the missing defense-in-depth/CSP CWE
    assert "CWE-693" in content or "CWE-116" in content or "CWE-346" in content, "CWE report is missing the correct CWE ID for protection mechanism failure / missing CSP (e.g., CWE-693)."

def test_admin_token_forged_correctly():
    """Verify that the admin token was correctly forged using cryptanalysis."""
    token_path = "/home/user/admin_token.txt"
    assert os.path.isfile(token_path), f"Admin token file missing at {token_path}"

    # Derive the expected token dynamically
    guest_plaintext = b"role=guest"
    guest_hex = "015c0f374e5416370047"
    guest_ciphertext = bytes.fromhex(guest_hex)

    # Recover key (assuming repeating XOR)
    key = bytes([guest_ciphertext[i] ^ guest_plaintext[i] for i in range(4)])

    admin_plaintext = b"role=admin"
    expected_admin_ciphertext = bytes([admin_plaintext[i] ^ key[i % len(key)] for i in range(len(admin_plaintext))])
    expected_admin_hex = expected_admin_ciphertext.hex()

    with open(token_path, "r") as f:
        actual_token = f.read().strip()

    assert actual_token == expected_admin_hex, f"Admin token is incorrect. Expected {expected_admin_hex}, got {actual_token}."

def test_csp_header_in_app():
    """Verify that the Content-Security-Policy header is added to app.py."""
    app_path = "/home/user/app/app.py"
    assert os.path.isfile(app_path), f"Application file missing at {app_path}"

    with open(app_path, "r") as f:
        content = f.read()

    expected_header_str = "Content-Security-Policy"
    expected_policy_str = "default-src 'self'; script-src 'self';"

    assert expected_header_str in content, "The Content-Security-Policy header name was not found in app.py."
    assert expected_policy_str in content, "The expected CSP policy string was not found in app.py."

def test_network_policy_updated():
    """Verify that the network policy was updated to allow localhost access to /admin."""
    policy_path = "/home/user/app/network_policy.json"
    assert os.path.isfile(policy_path), f"Network policy file missing at {policy_path}"

    with open(policy_path, "r") as f:
        try:
            policy = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("network_policy.json is not valid JSON.")

    rules = policy.get("firewall_rules", [])
    admin_rule = next((rule for rule in rules if rule.get("route") == "/admin"), None)

    assert admin_rule is not None, "The /admin route rule is missing from network_policy.json."
    assert admin_rule.get("action") == "ALLOW", "The action for the /admin route is not set to ALLOW."
    assert admin_rule.get("source_ip") == "127.0.0.1", "The source_ip for the /admin route is not set to 127.0.0.1."