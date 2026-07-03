# test_final_state.py
import os
import hashlib
import hmac
import pytest

def test_rotated_credentials_generated_correctly():
    output_path = "/home/user/rotated_credentials.csv"
    legacy_db_path = "/home/user/legacy_db.csv"
    wordlist_path = "/home/user/wordlist.txt"
    master_key_path = "/home/user/master.key"

    assert os.path.exists(output_path), f"Expected output file {output_path} is missing. Did the Rust program run and create it?"
    assert os.path.isfile(output_path), f"Path {output_path} exists but is not a regular file."

    # Read the master key
    assert os.path.exists(master_key_path), f"Master key file {master_key_path} is missing."
    with open(master_key_path, "rb") as f:
        master_key = f.read()

    # Read the wordlist and precompute hashes to simulate the cracking process
    assert os.path.exists(wordlist_path), f"Wordlist file {wordlist_path} is missing."
    with open(wordlist_path, "r") as f:
        words = f.read().splitlines()

    hash_to_plaintext = {}
    for word in words:
        sha256_hash = hashlib.sha256(word.encode('utf-8')).hexdigest()
        hash_to_plaintext[sha256_hash] = word

    # Read the legacy DB and derive the expected output
    assert os.path.exists(legacy_db_path), f"Legacy DB file {legacy_db_path} is missing."
    expected_lines = []
    with open(legacy_db_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) != 2:
                continue

            username, pw_hash = parts

            # If the password hash can be cracked using the wordlist
            if pw_hash in hash_to_plaintext:
                cracked_password = hash_to_plaintext[pw_hash]
                # Generate the HMAC-SHA256 token
                token = hmac.new(master_key, username.encode('utf-8'), hashlib.sha256).hexdigest()
                expected_lines.append(f"{username},{cracked_password},{token}")

    # The specifications require the output to be sorted alphabetically by username
    expected_lines.sort()

    # Read the actual output produced by the student's tool
    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    # Verify the results
    assert len(actual_lines) == len(expected_lines), (
        f"Output file {output_path} contains {len(actual_lines)} lines, "
        f"but expected {len(expected_lines)} lines based on successfully cracked users."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Line {i+1} in {output_path} is incorrect.\n"
            f"Expected: '{expected}'\n"
            f"Actual:   '{actual}'\n"
            "Ensure the format is 'username,cracked_password,new_token', the token is a lowercase hex HMAC-SHA256 digest, and lines are sorted alphabetically by username."
        )