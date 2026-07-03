# test_final_state.py

import os
import stat
import hashlib
import pytest

ROTATED_JSON_PATH = "/home/user/server/users_rotated.json"
SHA256_PATH = "/home/user/server/users_rotated.json.sha256"

EXPECTED_JSON_CONTENT = (
    '[{"token":"tok_111","username":"alice"},'
    '{"token":"7d5ec9268ab731ba2073994ab69cc3a38f3224b1bf82098d752f9b871c530517","username":"bob"},'
    '{"token":"e40733d7d74dbedc1f1ec7de5e2b0ba52ecba2f9a7cd6cf0ddc7dcf6dd629de0","username":"charlie"},'
    '{"token":"tok_444","username":"david"}]'
)

EXPECTED_HASH = "0e4af7890f5a287236dc9da8a5ef8c85ebdaab3818eebfe396bc75ce08c37107"

def test_users_rotated_json_exists_and_content():
    assert os.path.isfile(ROTATED_JSON_PATH), f"File {ROTATED_JSON_PATH} does not exist."

    with open(ROTATED_JSON_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == EXPECTED_JSON_CONTENT, (
        f"Content of {ROTATED_JSON_PATH} does not match the expected minified JSON string. "
        "Ensure the objects are sorted by username and keys are sorted alphabetically."
    )

def test_users_rotated_json_permissions():
    assert os.path.isfile(ROTATED_JSON_PATH), f"File {ROTATED_JSON_PATH} does not exist."

    st = os.stat(ROTATED_JSON_PATH)
    perms = stat.S_IMODE(st.st_mode)

    assert perms == 0o600, f"Permissions for {ROTATED_JSON_PATH} are {oct(perms)}, expected 0o600."

def test_users_rotated_sha256_file_exists_and_content():
    assert os.path.isfile(SHA256_PATH), f"File {SHA256_PATH} does not exist."

    with open(SHA256_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == EXPECTED_HASH, (
        f"Content of {SHA256_PATH} is incorrect. Expected {EXPECTED_HASH}, got {content}."
    )

def test_users_rotated_actual_sha256():
    assert os.path.isfile(ROTATED_JSON_PATH), f"File {ROTATED_JSON_PATH} does not exist."

    with open(ROTATED_JSON_PATH, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    assert actual_hash == EXPECTED_HASH, (
        f"Actual SHA256 of {ROTATED_JSON_PATH} ({actual_hash}) does not match the expected hash ({EXPECTED_HASH})."
    )