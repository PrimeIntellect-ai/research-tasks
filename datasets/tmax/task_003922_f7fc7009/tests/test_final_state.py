# test_final_state.py

import os
import hashlib
import pytest

def test_payload_bin():
    path = "/home/user/investigation/payload.bin"
    assert os.path.isfile(path), f"{path} does not exist. Did you run the compiled extractor?"

    with open(path, "rb") as f:
        content = f.read()

    expected_content = b"Secret_Payload_123!"
    assert content == expected_content, f"The content of {path} is incorrect. The timeline sorting or decryption might still be flawed."

def test_flag_txt():
    path = "/home/user/investigation/flag.txt"
    assert os.path.isfile(path), f"{path} does not exist. Did you save the SHA-256 hash?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_hash = hashlib.sha256(b"Secret_Payload_123!").hexdigest()
    assert content == expected_hash, f"The hash in {path} does not match the expected SHA-256 hash of the payload."