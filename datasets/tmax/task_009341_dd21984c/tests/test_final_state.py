# test_final_state.py
import os
import json
import hashlib
import pytest

RESULTS_FILE = "/home/user/audit_results.json"
XOR_KEY = 0x5A
EXPECTED_FLAG = "FLAG{x0r_md5_w34k_cryst0_f4il}"
EXPECTED_HEADER = "content-security-policy"

@pytest.fixture
def audit_results():
    assert os.path.isfile(RESULTS_FILE), f"The file {RESULTS_FILE} does not exist. Did you save your findings?"

    with open(RESULTS_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {RESULTS_FILE} does not contain valid JSON.")

    required_keys = {"admin_token", "flag", "missing_security_header"}
    missing_keys = required_keys - set(data.keys())
    assert not missing_keys, f"The JSON in {RESULTS_FILE} is missing required keys: {', '.join(missing_keys)}"

    return data

def test_missing_security_header(audit_results):
    """Verify that the correct missing security header was identified."""
    header = audit_results.get("missing_security_header", "")
    assert isinstance(header, str), "The missing_security_header value must be a string."
    assert header.lower() == EXPECTED_HEADER, f"The identified missing header '{header}' is incorrect."

def test_flag_retrieval(audit_results):
    """Verify that the correct flag was retrieved."""
    flag = audit_results.get("flag", "")
    assert flag == EXPECTED_FLAG, f"The retrieved flag '{flag}' is incorrect."

def test_admin_token_validity(audit_results):
    """Verify that the crafted admin token is valid, properly signed, and grants admin privileges."""
    token_hex = audit_results.get("admin_token", "")
    assert isinstance(token_hex, str), "The admin_token value must be a string."

    try:
        raw_data = bytes.fromhex(token_hex)
    except ValueError:
        pytest.fail("The admin_token is not a valid hex string.")

    assert len(raw_data) > 16, "The admin_token is too short to contain both ciphertext and an MD5 hash."

    ciphertext = raw_data[:-16]
    provided_hash = raw_data[-16:]

    # Verify MD5 checksum
    calculated_hash = hashlib.md5(ciphertext).digest()
    assert calculated_hash == provided_hash, "The MD5 checksum appended to the token is incorrect for the given ciphertext."

    # Decrypt and verify JSON payload
    try:
        plaintext = bytes([b ^ XOR_KEY for b in ciphertext])
        session_data = json.loads(plaintext.decode('utf-8'))
    except UnicodeDecodeError:
        pytest.fail("The decrypted token does not contain valid UTF-8 text.")
    except json.JSONDecodeError:
        pytest.fail("The decrypted token does not contain valid JSON.")

    assert session_data.get("admin") is True, "The decrypted token does not contain '\"admin\": true'."