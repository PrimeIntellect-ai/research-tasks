# test_final_state.py

import os
import base64
import hashlib
import pytest

LOG_FILE = "/home/user/tampered.log"
ARTIFACTS_DIR = "/home/user/artifacts"

def get_expected_tampered_log():
    tampered_entries = []

    if not os.path.exists(ARTIFACTS_DIR):
        return ""

    for filename in os.listdir(ARTIFACTS_DIR):
        filepath = os.path.join(ARTIFACTS_DIR, filename)
        if not os.path.isfile(filepath):
            continue

        with open(filepath, 'r') as f:
            lines = f.read().strip().split('\n')

        checksum = None
        payload_b64 = None
        for line in lines:
            if line.startswith("Checksum:"):
                checksum = line.split(":", 1)[1].strip()
            elif line.startswith("Payload:"):
                payload_b64 = line.split(":", 1)[1].strip()

        if checksum and payload_b64:
            decoded_bytes = base64.b64decode(payload_b64)
            calculated_hash = hashlib.sha256(decoded_bytes).hexdigest()

            if calculated_hash != checksum:
                tampered_entries.append(f"{filename}:{decoded_bytes.hex()}")

    tampered_entries.sort()
    if not tampered_entries:
        return ""
    return "\n".join(tampered_entries) + "\n"

def test_tampered_log_exists():
    assert os.path.exists(LOG_FILE), f"The log file {LOG_FILE} was not created."
    assert os.path.isfile(LOG_FILE), f"{LOG_FILE} is not a regular file."

def test_tampered_log_contents():
    expected_content = get_expected_tampered_log()

    with open(LOG_FILE, 'r') as f:
        actual_content = f.read()

    # Standardize line endings for comparison
    actual_content_normalized = actual_content.strip() + "\n" if actual_content.strip() else ""
    expected_content_normalized = expected_content.strip() + "\n" if expected_content.strip() else ""

    assert actual_content_normalized == expected_content_normalized, (
        f"The contents of {LOG_FILE} do not match the expected output.\n"
        f"Expected:\n{expected_content_normalized}\n"
        f"Actual:\n{actual_content_normalized}"
    )