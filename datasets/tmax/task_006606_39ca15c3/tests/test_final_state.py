# test_final_state.py
import os

def test_resolution_file_content():
    resolution_path = "/home/user/incident-104/resolution.txt"
    assert os.path.exists(resolution_path), f"File {resolution_path} does not exist. Did you save the final hash?"

    with open(resolution_path, "r") as f:
        content = f.read().strip()

    expected_hash = "SUCCESS_HASH_12"
    assert expected_hash in content, f"Expected {resolution_path} to contain '{expected_hash}', but found: '{content}'"

def test_secret_token_file():
    secret_token_path = "/home/user/incident-104/.secret_token"
    assert os.path.exists(secret_token_path), f"File {secret_token_path} does not exist. Did you find the missing initialization file path?"

    with open(secret_token_path, "r") as f:
        content = f.read().strip()

    expected_token = "TOKEN_8f9a2b4c6d"
    assert content.startswith(expected_token), f"Expected {secret_token_path} to contain the token '{expected_token}'"