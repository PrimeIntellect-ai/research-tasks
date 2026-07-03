# test_final_state.py
import os
import stat
import subprocess
import hmac
import hashlib
import base64
import pytest

PAYLOAD_FILE = "/home/user/payload.out"
SCRIPT_FILE = "/home/user/craft_payload.sh"

def test_script_exists_and_permissions():
    """Test that the script exists and has 700 permissions."""
    assert os.path.exists(SCRIPT_FILE), f"Fail: {SCRIPT_FILE} not found."
    assert os.path.isfile(SCRIPT_FILE), f"Fail: {SCRIPT_FILE} is not a file."

    st = os.stat(SCRIPT_FILE)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Fail: Script permissions are not 700. Found: {oct(perms)}"

def test_payload_file_exists():
    """Test that the payload output file was generated."""
    assert os.path.exists(PAYLOAD_FILE), f"Fail: {PAYLOAD_FILE} not found."
    assert os.path.isfile(PAYLOAD_FILE), f"Fail: {PAYLOAD_FILE} is not a file."

def test_payload_format_and_hmac():
    """Test that the payload file has the correct format and the HMAC is valid."""
    with open(PAYLOAD_FILE, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) >= 2, "Fail: Payload file must contain at least two lines (HMAC and DATA)."

    hmac_line = next((line for line in lines if line.startswith("HMAC:")), None)
    data_line = next((line for line in lines if line.startswith("DATA:")), None)

    assert hmac_line is not None, "Fail: Missing HMAC line starting with 'HMAC:'."
    assert data_line is not None, "Fail: Missing DATA line starting with 'DATA:'."

    extracted_hmac = hmac_line[5:].strip()
    extracted_data = data_line[5:].strip()

    assert extracted_hmac, "Fail: Missing HMAC value."
    assert extracted_data, "Fail: Missing DATA value."

    # Verify HMAC using Python standard library
    secret = b"RedTeamC2Secret"
    calculated_hmac = hmac.new(secret, extracted_data.encode('utf-8'), hashlib.sha256).hexdigest()

    assert extracted_hmac == calculated_hmac, f"Fail: HMAC verification failed. Expected {calculated_hmac}, got {extracted_hmac}"

def test_decryption_and_redaction():
    """Test that the payload data can be decrypted and matches the expected redacted content."""
    with open(PAYLOAD_FILE, "r") as f:
        lines = f.read().strip().split('\n')

    data_line = next((line for line in lines if line.startswith("DATA:")), None)
    assert data_line is not None, "Fail: Missing DATA line in payload."
    extracted_data = data_line[5:].strip()

    try:
        binary_data = base64.b64decode(extracted_data)
    except Exception as e:
        pytest.fail(f"Fail: DATA is not valid Base64. Error: {e}")

    # Decrypt using openssl via subprocess to match the verification script's exact method
    process = subprocess.run(
        ["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-pass", "pass:Evasion2024!"],
        input=binary_data,
        capture_output=True
    )

    assert process.returncode == 0, f"Fail: Decryption failed. Incorrect password or method. OpenSSL error: {process.stderr.decode('utf-8')}"

    decrypted_text = process.stdout.decode('utf-8')

    expected_text = """Target System Compromised.
Admin IP: [REDACTED_IP]
Backup Server: [REDACTED_IP]
User data found:
Alice - [REDACTED_SSN] - Admin
Bob - [REDACTED_SSN] - User
Network subnet: [REDACTED_IP]"""

    assert decrypted_text.strip() == expected_text.strip(), "Fail: Redacted content does not match expectations."