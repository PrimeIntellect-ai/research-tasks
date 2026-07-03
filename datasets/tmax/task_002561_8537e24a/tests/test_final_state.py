# test_final_state.py

import os
import subprocess
import binascii

def test_validator_compiled():
    binary_path = "/home/user/validator"
    assert os.path.isfile(binary_path), f"The compiled binary '{binary_path}' is missing. Did you compile validator.c?"
    assert os.access(binary_path, os.X_OK), f"The file '{binary_path}' is not executable."

def test_cert_verify_log():
    log_path = "/home/user/cert_verify.log"
    assert os.path.isfile(log_path), f"The certificate verification log '{log_path}' is missing."

    with open(log_path, 'r') as f:
        log_content = f.read()

    assert "OK" in log_content, f"The log file '{log_path}' does not contain 'OK'. Ensure you verified the certificate correctly."

def test_forged_token_exists_and_valid():
    token_path = "/home/user/forged_token.txt"
    assert os.path.isfile(token_path), f"The forged token file '{token_path}' is missing."

    with open(token_path, 'r') as f:
        token = f.read().strip()

    assert token, "The forged token file is empty."

    parts = token.split('.')
    assert len(parts) == 3, "The token does not have the correct format: <Header>.<Payload>.<Signature>"

    header_hex, payload_hex, sig_hex = parts

    try:
        header_bytes = binascii.unhexlify(header_hex)
        payload_bytes = binascii.unhexlify(payload_hex)
    except binascii.Error:
        assert False, "The header and payload must be valid hex-encoded strings."

    header_str = header_bytes.decode('ascii', errors='ignore')
    assert '"alg":"none"' in header_str, "The token header does not contain the bypass string '\"alg\":\"none\"'."

    # Decrypt payload using XOR key 0x5A
    decrypted_payload = bytes([b ^ 0x5A for b in payload_bytes]).decode('ascii', errors='ignore')
    assert '"role":"admin"' in decrypted_payload, "The decrypted payload does not contain '\"role\":\"admin\"'."

def test_validator_execution_with_token():
    binary_path = "/home/user/validator"
    token_path = "/home/user/forged_token.txt"

    if not os.path.isfile(binary_path) or not os.path.isfile(token_path):
        return # Handled by previous tests

    with open(token_path, 'r') as f:
        token = f.read().strip()

    result = subprocess.run([binary_path, token], capture_output=True, text=True)

    assert "Access Granted: Admin" in result.stdout, (
        f"Running the validator with the forged token did not grant admin access.\n"
        f"Output was: {result.stdout.strip()}"
    )