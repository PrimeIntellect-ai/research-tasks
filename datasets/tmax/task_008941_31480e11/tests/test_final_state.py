# test_final_state.py
import os
import subprocess
import pytest

def get_fingerprint(pubkey_path):
    try:
        output = subprocess.check_output(['ssh-keygen', '-l', '-f', pubkey_path], text=True)
        # Output format: "2048 SHA256:... user@host (RSA)"
        return output.split()[1]
    except Exception as e:
        pytest.fail(f"Failed to get fingerprint for {pubkey_path}: {e}")

def get_token_validity():
    tokens_file = "/home/user/tokens.txt"
    if not os.path.exists(tokens_file):
        pytest.fail(f"{tokens_file} is missing.")

    validity = {}
    with open(tokens_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":")
            if len(parts) == 3:
                username, timestamp, expected_checksum = parts
                actual_sum = sum(ord(c) for c in username + timestamp)
                is_valid = (actual_sum % 256) == int(expected_checksum)
                validity[username] = "Yes" if is_valid else "No"
    return validity

def test_c_program_exists():
    assert os.path.isfile("/home/user/validate.c"), "/home/user/validate.c is missing."
    assert os.path.isfile("/home/user/validate"), "/home/user/validate executable is missing."
    assert os.access("/home/user/validate", os.X_OK), "/home/user/validate is not executable."

def test_compliance_audit_csv():
    audit_file = "/home/user/compliance_audit.csv"
    assert os.path.isfile(audit_file), f"{audit_file} is missing."

    # Map fingerprints to users
    pubkeys_dir = "/home/user/pubkeys"
    fp_to_user = {}
    for filename in os.listdir(pubkeys_dir):
        if filename.endswith(".pub"):
            username = filename[:-4]
            fp = get_fingerprint(os.path.join(pubkeys_dir, filename))
            fp_to_user[fp] = username

    token_validity = get_token_validity()

    # Parse auth events
    expected_lines = []
    auth_file = "/home/user/auth_events.log"
    with open(auth_file, "r") as f:
        for line in f:
            if "Accepted publickey" in line:
                parts = line.strip().split()
                fp = parts[-1]
                username = fp_to_user.get(fp)
                if not username:
                    pytest.fail(f"Fingerprint {fp} found in log but does not match any public key.")

                valid = token_validity.get(username, "No")
                expected_lines.append(f"{username},{fp},{valid}")

    # Read actual CSV
    with open(audit_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} rows in CSV, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Row {i+1} mismatch. Expected: '{expected}', Got: '{actual}'"