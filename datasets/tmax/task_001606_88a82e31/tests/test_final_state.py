# test_final_state.py

import os
import pytest

def test_clean_log_exists():
    """Verify that the clean_log.txt file was created."""
    file_path = "/home/user/evidence/clean_log.txt"
    assert os.path.isfile(file_path), f"File missing: {file_path}"

def test_clean_log_content():
    """Verify that the clean_log.txt file contains the correctly redacted log."""
    file_path = "/home/user/evidence/clean_log.txt"
    assert os.path.isfile(file_path), f"File missing: {file_path}"

    expected_content = (
        "GET /login?user=admin&password=REDACTED&redirect=http://evil.com/log HTTP/1.1\n"
        "Host: example.com\n"
        "User-Agent: Mozilla/5.0\n"
        "\n"
        "GET /login?user=jsmith&password=REDACTED&redirect=http://evil.com/log HTTP/1.1\n"
        "Host: example.com\n"
        "User-Agent: curl/7.68.0\n"
    )

    with open(file_path, "r", encoding="utf-8") as f:
        actual_content = f.read()

    assert actual_content == expected_content, (
        "The contents of clean_log.txt do not match the expected redacted log. "
        "Check your extraction, decryption, and redaction logic."
    )