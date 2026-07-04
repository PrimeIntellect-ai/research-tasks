# test_final_state.py
import os
import hashlib
import pytest

def test_payload_txt():
    payload_path = "/home/user/payload.txt"
    assert os.path.isfile(payload_path), f"File {payload_path} does not exist."

    with open(payload_path, "r") as f:
        payload = f.read().strip()

    assert not payload.startswith("../"), "Payload must bypass the naive '../' check."

    target_path = os.path.abspath(os.path.join("/home/user/vuln_app/uploads", payload))
    expected_path = "/home/user/vuln_app/pwned.txt"
    assert target_path == expected_path, f"Payload resolves to {target_path}, expected {expected_path}."

def test_redacted_txt():
    redacted_path = "/home/user/redacted.txt"
    assert os.path.isfile(redacted_path), f"File {redacted_path} does not exist."

    expected_content = (
        "User: alice, CC: XXXX-XXXX-XXXX-XXXX, Role: Admin\n"
        "User: bob, CC: XXXX-XXXX-XXXX-XXXX, Role: User\n"
        "User: charlie, CC: XXXX-XXXX-XXXX-XXXX, Role: Moderator\n"
        "User: dave, CC: XXXX-XXXX-XXXX-XXXX, Role: User\n"
    )

    with open(redacted_path, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), "The redacted.txt content does not match the expected redacted output."

def test_hash_txt():
    redacted_path = "/home/user/redacted.txt"
    hash_path = "/home/user/hash.txt"

    assert os.path.isfile(redacted_path), f"File {redacted_path} does not exist."
    assert os.path.isfile(hash_path), f"File {hash_path} does not exist."

    with open(redacted_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    with open(hash_path, "r") as f:
        hash_content = f.read().strip()

    expected_hash_line = f"{file_hash}  {redacted_path}"

    # sha256sum output usually has two spaces, but we can just check if the hash is present and correct
    assert hash_content.startswith(file_hash), "hash.txt does not start with the correct SHA-256 hash."
    assert redacted_path in hash_content, f"hash.txt does not contain the filename {redacted_path}."