# test_final_state.py

import os
import sys
import pytest

PAYLOAD_PATH = '/home/user/payload.txt'
DEOBFUSCATOR_DIR = '/home/user'

def test_payload_file_exists():
    """Test that the payload.txt file exists."""
    assert os.path.exists(PAYLOAD_PATH), f"The file {PAYLOAD_PATH} does not exist. You must write your payload here."
    assert os.path.isfile(PAYLOAD_PATH), f"The path {PAYLOAD_PATH} is not a file."

def test_payload_no_e():
    """Test that the payload does not contain the characters 'e' or 'E'."""
    with open(PAYLOAD_PATH, 'r') as f:
        payload = f.read().strip()

    assert payload, "The payload file is empty."
    assert 'e' not in payload, "The payload contains the forbidden lowercase letter 'e'."
    assert 'E' not in payload, "The payload contains the forbidden uppercase letter 'E'."

def test_payload_deobfuscates_correctly():
    """Test that the payload deobfuscates to the correct URL."""
    with open(PAYLOAD_PATH, 'r') as f:
        payload = f.read().strip()

    # Dynamically import the deobfuscate module
    sys.path.insert(0, DEOBFUSCATOR_DIR)
    try:
        import deobfuscate
    except ImportError:
        pytest.fail(f"Could not import deobfuscate.py from {DEOBFUSCATOR_DIR}.")

    try:
        decrypted_url = deobfuscate.decrypt_url(payload)
    except Exception as e:
        pytest.fail(f"Failed to deobfuscate the payload. Error: {e}")

    expected_prefix = "http://redteam.htb/capture"
    assert decrypted_url.startswith(expected_prefix), (
        f"The deobfuscated URL does not start with the required prefix.\n"
        f"Expected prefix: {expected_prefix}\n"
        f"Actual URL: {decrypted_url}"
    )