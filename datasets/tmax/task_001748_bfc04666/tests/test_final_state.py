# test_final_state.py

import os
import re
import pytest

def test_token_extracted_correctly():
    core_bin_path = "/home/user/core.bin"
    token_txt_path = "/home/user/token.txt"

    assert os.path.isfile(core_bin_path), f"File {core_bin_path} is missing."
    assert os.path.isfile(token_txt_path), f"File {token_txt_path} was not created."

    # Extract expected token from core.bin
    with open(core_bin_path, "rb") as f:
        core_data = f.read()

    match = re.search(b"SECRET_TOKEN=([a-zA-Z0-9-]+)", core_data)
    assert match is not None, "Could not find SECRET_TOKEN in core.bin."
    expected_token = match.group(1).decode("utf-8")

    with open(token_txt_path, "r", encoding="utf-8") as f:
        actual_token = f.read().strip()

    assert actual_token == expected_token, f"Token in {token_txt_path} is incorrect. Expected '{expected_token}', got '{actual_token}'."

def test_clean_logs_generated_correctly():
    clean_logs_path = "/home/user/clean_logs.txt"
    assert os.path.isfile(clean_logs_path), f"File {clean_logs_path} was not created."

    expected_logs = [
        "INFO: Service started",
        "WARN: High memory usage",
        "CRITICAL: Memory corruption detected",
        "INFO: Service stopping"
    ]

    with open(clean_logs_path, "r", encoding="utf-8") as f:
        actual_logs = [line.strip() for line in f if line.strip()]

    assert actual_logs == expected_logs, f"Logs in {clean_logs_path} do not match the expected output. Got: {actual_logs}"