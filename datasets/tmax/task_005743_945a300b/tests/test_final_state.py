# test_final_state.py

import os
import hashlib
import pytest

def test_redacted_capture_log():
    path = "/home/user/evidence/redacted_capture.log"
    assert os.path.isfile(path), f"The file {path} was not created."

    with open(path, 'r') as f:
        content = f.read()

    # Check that redactions were applied correctly
    expected_cookie_1 = "Cookie: theme=dark; session_token=[REDACTED]; password=[REDACTED]"
    expected_cookie_2 = "Cookie: session_token=[REDACTED]; theme=light"

    assert expected_cookie_1 in content, f"{path} does not contain the correctly redacted first cookie."
    assert expected_cookie_2 in content, f"{path} does not contain the correctly redacted second cookie."

    # Check that original sensitive data is gone
    assert "abc123def456" not in content, f"{path} still contains the original session_token from the first request."
    assert "supersecret" not in content, f"{path} still contains the original password from the first request."
    assert "hacker999" not in content, f"{path} still contains the original session_token from the second request."

def test_recovered_txt():
    path = "/home/user/evidence/recovered.txt"
    assert os.path.isfile(path), f"The file {path} was not created. Decryption may have failed."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_content = "CONFIDENTIAL_PROJECT_OMEGA_BLUEPRINTS_V1"
    assert content == expected_content, f"The content of {path} is incorrect. Found: '{content}'"

def test_hash_txt():
    path = "/home/user/evidence/hash.txt"
    assert os.path.isfile(path), f"The file {path} was not created."

    with open(path, 'r') as f:
        content = f.read().strip()

    # Compute the expected hash dynamically based on the expected recovered content
    expected_text = "CONFIDENTIAL_PROJECT_OMEGA_BLUEPRINTS_V1"
    expected_hash = hashlib.sha256(expected_text.encode('utf-8')).hexdigest()

    assert content == expected_hash, f"The hash in {path} is incorrect. Expected: {expected_hash}, Found: {content}"