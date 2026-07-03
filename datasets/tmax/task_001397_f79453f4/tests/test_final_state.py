# test_final_state.py
import os
import json
import base64
import pytest

def test_revocation_list_encrypted_correctly():
    log_path = "/home/user/access.log"
    key_path = "/home/user/rotation_key.key"
    enc_path = "/home/user/revocation_list.enc"

    assert os.path.exists(log_path), f"Log file missing: {log_path}"
    assert os.path.exists(key_path), f"Key file missing: {key_path}"
    assert os.path.exists(enc_path), f"Encrypted output file missing: {enc_path}"

    # Recompute the expected compromised users from the log file
    compromised_users = set()
    with open(log_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                log_entry = json.loads(line)
                auth_header = log_entry.get("headers", {}).get("Authorization", "")
                if auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]
                    parts = token.split(".")
                    if len(parts) >= 2:
                        # Decode header
                        header_padded = parts[0] + "=" * ((4 - len(parts[0]) % 4) % 4)
                        header_json = base64.urlsafe_b64decode(header_padded).decode("utf-8")
                        header = json.loads(header_json)

                        alg = header.get("alg", "")
                        if alg.lower() == "none":
                            # Decode payload
                            payload_padded = parts[1] + "=" * ((4 - len(parts[1]) % 4) % 4)
                            payload_json = base64.urlsafe_b64decode(payload_padded).decode("utf-8")
                            payload = json.loads(payload_json)
                            if "username" in payload:
                                compromised_users.add(payload["username"])
            except Exception:
                pass

    expected_plaintext = ",".join(sorted(list(compromised_users)))

    # Decrypt the output file using the provided key
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        pytest.fail("The 'cryptography' package is missing but required for verification.")

    with open(key_path, "rb") as f:
        key = f.read()

    fernet = Fernet(key)

    with open(enc_path, "rb") as f:
        encrypted_data = f.read()

    try:
        decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8")
    except Exception as e:
        pytest.fail(f"Failed to decrypt {enc_path}. Is it a valid Fernet token encrypted with the correct key? Error: {e}")

    assert decrypted_data == expected_plaintext, (
        f"Decrypted data does not match expected compromised users. "
        f"Expected '{expected_plaintext}', got '{decrypted_data}'"
    )