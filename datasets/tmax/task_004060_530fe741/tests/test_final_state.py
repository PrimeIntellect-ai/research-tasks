# test_final_state.py
import os
import hashlib

def test_extracted_flag_matches_original():
    """Validates that the extracted flag exactly matches the original flag file."""
    flag_path = "/home/user/flag.txt"
    extracted_path = "/home/user/extracted_flag.txt"

    assert os.path.exists(flag_path), f"Original flag file {flag_path} is missing."
    assert os.path.exists(extracted_path), f"Extracted flag file {extracted_path} was not created."

    with open(flag_path, 'rb') as f:
        expected_content = f.read()

    with open(extracted_path, 'rb') as f:
        extracted_content = f.read()

    assert extracted_content == expected_content, (
        "The contents of the extracted flag file do not exactly match the original flag. "
        "Ensure no extra characters or missing newlines are present."
    )

def test_flag_hash_is_correct():
    """Validates that the computed hash matches the SHA256 of the flag content."""
    flag_path = "/home/user/flag.txt"
    hash_path = "/home/user/flag_hash.txt"

    assert os.path.exists(flag_path), f"Original flag file {flag_path} is missing."
    assert os.path.exists(hash_path), f"Flag hash file {hash_path} was not created."

    with open(flag_path, 'rb') as f:
        flag_content = f.read()

    expected_hash = hashlib.sha256(flag_content).hexdigest()

    with open(hash_path, 'r') as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, (
        f"The hash in {hash_path} is incorrect. "
        f"Expected {expected_hash}, but got {actual_hash}."
    )