# test_final_state.py
import os
import stat
import base64
import hashlib
import json

TOKEN_PATH = "/home/user/evasion.token"
REPORT_PATH = "/home/user/exfiltration_report.txt"

def test_evasion_token_permissions():
    assert os.path.exists(TOKEN_PATH), f"Token file missing at {TOKEN_PATH}"

    # Check permissions (octal 0400)
    st = os.stat(TOKEN_PATH)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Expected permissions 0o400 for {TOKEN_PATH}, got {oct(perms)}"

def test_evasion_token_content():
    assert os.path.exists(TOKEN_PATH), f"Token file missing at {TOKEN_PATH}"

    with open(TOKEN_PATH, "rb") as f:
        token_bytes = f.read()

    assert not token_bytes.endswith(b"\n"), "Token file should not have a trailing newline."

    token_str = token_bytes.decode('utf-8')
    parts = token_str.split('.')
    assert len(parts) == 3, "Token must be in header.payload.signature format."

    header_b64, payload_b64, signature_b64 = parts

    # Signature should be empty or bypassable, but instructions say "leaving the signature empty"
    assert signature_b64 == "", "Signature part of the token should be empty."

    # Decode header
    try:
        # Add padding if missing
        header_padded = header_b64 + '=' * (-len(header_b64) % 4)
        header_json = base64.b64decode(header_padded).decode('utf-8')
    except Exception as e:
        assert False, f"Failed to base64 decode header: {e}"

    assert '"alg":"none"' in header_json.replace(' ', ''), 'Header must contain "alg":"none"'

    # Decode payload
    try:
        payload_padded = payload_b64 + '=' * (-len(payload_b64) % 4)
        payload_json = base64.b64decode(payload_padded).decode('utf-8')
    except Exception as e:
        assert False, f"Failed to base64 decode payload: {e}"

    try:
        payload_dict = json.loads(payload_json)
        assert payload_dict.get("role") == "admin", 'Payload must decode to exactly {"role":"admin"}'
    except json.JSONDecodeError:
        assert '"role":"admin"' in payload_json.replace(' ', ''), 'Payload must contain "role":"admin"'

def test_report_content():
    assert os.path.exists(REPORT_PATH), f"Report file missing at {REPORT_PATH}"

    with open(REPORT_PATH, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, "Report file must contain at least two lines."

    cwe_line = lines[0].strip()
    hash_line = lines[1].strip()

    assert cwe_line == "CWE-347", f"Expected first line to be CWE-347, got {cwe_line}"

    # Verify the hash matches the actual token file content
    assert os.path.exists(TOKEN_PATH), f"Token file missing at {TOKEN_PATH}"
    with open(TOKEN_PATH, "rb") as f:
        token_bytes = f.read()

    expected_hash = hashlib.sha256(token_bytes).hexdigest()
    assert hash_line == expected_hash, f"Expected hash {expected_hash}, got {hash_line}"