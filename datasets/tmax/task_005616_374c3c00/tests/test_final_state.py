# test_final_state.py

import os
import sys
import json
import binascii
import pytest

def test_admin_token_valid():
    """Test that the admin token is correctly generated and saved."""
    token_path = '/home/user/admin_token.txt'
    assert os.path.exists(token_path), f"File {token_path} does not exist. Did you save the admin token?"

    with open(token_path, 'r') as f:
        hex_data = f.read().strip()

    assert hex_data, f"File {token_path} is empty."

    try:
        ciphertext = binascii.unhexlify(hex_data)
    except binascii.Error as e:
        pytest.fail(f"Contents of {token_path} are not valid hex: {e}")

    # Import the service module to use its decryption logic
    vault_dir = '/home/user/vault'
    if vault_dir not in sys.path:
        sys.path.insert(0, vault_dir)

    try:
        import service
    except ImportError as e:
        pytest.fail(f"Could not import service.py from {vault_dir}: {e}")

    # The PIN used in the setup is 7391
    expected_pin = '7391'

    try:
        payload = service.decrypt_token(ciphertext, expected_pin)
    except Exception as e:
        pytest.fail(f"Failed to decrypt the token using the correct PIN. Is it encrypted properly? Error: {e}")

    assert isinstance(payload, dict), f"Decrypted payload is not a JSON object, got: {type(payload)}"
    assert payload.get('user') == 'admin', f"Expected user 'admin', but got '{payload.get('user')}'"
    assert payload.get('role') == 'root', f"Expected role 'root', but got '{payload.get('role')}'"