# test_final_state.py

import os
import pytest

CRITICAL_LOG = "/home/user/critical.log"

EXPECTED_CONTENT = """[ERROR]
Database connection failed
Timeout: 30s
Module: Auth
[/ERROR]
[ERROR]
Disk full
Path: /var/log
Module: Storage
[/ERROR]
"""

def test_critical_log_exists():
    assert os.path.exists(CRITICAL_LOG), f"File {CRITICAL_LOG} does not exist."
    assert os.path.isfile(CRITICAL_LOG), f"{CRITICAL_LOG} is not a regular file."

def test_critical_log_content_and_encoding():
    # Attempt to read as UTF-8
    try:
        with open(CRITICAL_LOG, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        pytest.fail(f"{CRITICAL_LOG} is not properly UTF-8 encoded.")

    # Normalize line endings for robust comparison
    content_normalized = content.replace("\r\n", "\n").strip()
    expected_normalized = EXPECTED_CONTENT.replace("\r\n", "\n").strip()

    assert content_normalized == expected_normalized, (
        f"Content of {CRITICAL_LOG} does not match expected output.\n"
        f"Expected:\n{expected_normalized}\n\n"
        f"Got:\n{content_normalized}"
    )