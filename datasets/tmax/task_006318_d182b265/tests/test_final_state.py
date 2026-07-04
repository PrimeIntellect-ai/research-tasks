# test_final_state.py
import os
import base64
import hmac
import hashlib
import json

def test_final_payload_exists():
    """Verify that the final_payload.txt file was created."""
    assert os.path.isfile("/home/user/final_payload.txt"), "/home/user/final_payload.txt does not exist."

def test_final_payload_validity():
    """Verify the structure, signature, and contents of the generated JWT."""
    with open("/home/user/final_payload.txt", "r") as f:
        token = f.read().strip()

    parts = token.split('.')
    assert len(parts) == 3, f"Expected a valid JWT with 3 parts (Header.Payload.Signature), but found {len(parts)} parts."

    head, pld, sig = parts

    # 1. Verify the HMAC-SHA256 signature
    secret = b"operator_secret_2024!"
    signing_input = f"{head}.{pld}".encode()
    expected_sig_bytes = hmac.new(secret, signing_input, hashlib.sha256).digest()
    expected_sig = base64.urlsafe_b64encode(expected_sig_bytes).decode().rstrip('=')

    assert sig == expected_sig, "The JWT signature is invalid. Ensure you are using HMAC-SHA256 with the correct secret."

    # 2. Decode and verify the payload
    # Add padding for base64 decoding
    pld_padded = pld + "=" * ((4 - len(pld) % 4) % 4)
    try:
        decoded_pld_bytes = base64.urlsafe_b64decode(pld_padded)
        decoded_pld = json.loads(decoded_pld_bytes.decode('utf-8'))
    except Exception as e:
        assert False, f"Failed to decode or parse the JWT payload as JSON: {e}"

    assert decoded_pld.get('user') == 'admin', f"Expected user to be 'admin', but got '{decoded_pld.get('user')}'."

    redirect_val = decoded_pld.get('redirect')
    assert redirect_val is not None, "The 'redirect' field is missing from the JWT payload."

    # 3. Verify the XOR-encoded and Base64url-encoded redirect payload
    url = "gopher://127.0.0.1:8080/_POST%20/admin/shutdown"
    key = [0xDE, 0xAD, 0xBE, 0xEF]

    xored = bytearray()
    for i, c in enumerate(url):
        xored.append(ord(c) ^ key[i % 4])

    expected_redirect = base64.urlsafe_b64encode(xored).decode().rstrip('=')

    assert redirect_val == expected_redirect, (
        f"The 'redirect' value does not match the expected encoded string.\n"
        f"Expected: {expected_redirect}\n"
        f"Actual:   {redirect_val}"
    )