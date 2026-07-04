# test_final_state.py

import os
import hashlib
import base64

def test_recovered_dat_exists_and_correct():
    path = "/home/user/recovered.dat"
    assert os.path.isfile(path), f"Missing file: {path}. Did you successfully run the compiled backdoor?"

    expected_content = base64.b64decode("Q09ORklERU5USUFMX0ZPUkVOU0lDX0RBVEFfNzc4ODk5Cg==")
    with open(path, "rb") as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"The content of {path} does not match the expected decrypted evidence."

def test_evidence_hash_txt():
    path = "/home/user/evidence_hash.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    expected_content = base64.b64decode("Q09ORklERU5USUFMX0ZPUkVOU0lDX0RBVEFfNzc4ODk5Cg==")
    expected_hash = hashlib.sha256(expected_content).hexdigest()

    with open(path, "r") as f:
        actual_hash = f.read().strip()

    # In case they used `sha256sum recovered.dat > evidence_hash.txt`, it might contain the filename.
    # We take the first word.
    actual_hash = actual_hash.split()[0] if actual_hash else ""

    assert actual_hash == expected_hash, f"The hash in {path} is incorrect. Expected {expected_hash}, got {actual_hash}."