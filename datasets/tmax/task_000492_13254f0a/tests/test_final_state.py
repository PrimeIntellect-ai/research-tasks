# test_final_state.py

import os
import hashlib
import pytest

def test_rotation_report_exists():
    assert os.path.isfile("/home/user/rotation_report.txt"), "The file /home/user/rotation_report.txt was not created."

def test_rotation_report_content():
    # Recompute the expected hash based on the known leaked key from the setup
    expected_key = b"sk_live_9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c"
    expected_hash = hashlib.sha256(expected_key).hexdigest()

    with open("/home/user/rotation_report.txt", "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) >= 2, "/home/user/rotation_report.txt must contain at least two lines."

    # Check for the OLD_KEY_HASH
    expected_hash_line = f"OLD_KEY_HASH={expected_hash}"
    assert any(line.strip() == expected_hash_line for line in content), f"Could not find exact line '{expected_hash_line}' in rotation_report.txt."

    # Check for NEW_CODE_CWE
    # The vulnerability is Cross-Site Scripting (XSS), which is CWE-79
    expected_cwe_line = "NEW_CODE_CWE=CWE-79"
    assert any(line.strip().upper() == expected_cwe_line for line in content), f"Could not find line '{expected_cwe_line}' (case-insensitive on CWE-79) in rotation_report.txt."

def test_access_log_redacted():
    assert os.path.isfile("/home/user/logs/access.log"), "/home/user/logs/access.log is missing."

    with open("/home/user/logs/access.log", "r") as f:
        content = f.read()

    old_key = "sk_live_9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c"

    # The old key should be completely removed
    assert old_key not in content, "The old API key is still present in /home/user/logs/access.log."
    assert "sk_live_" not in content, "Found remnants of 'sk_live_' keys in /home/user/logs/access.log."

    # The key should be replaced with [REDACTED]
    assert "[REDACTED]" in content, "The literal string '[REDACTED]' was not found in /home/user/logs/access.log."

    # Ensure the rest of the log structure remains unchanged
    assert "GET /api/data?key=[REDACTED] HTTP/1.1" in content, "The log lines were not redacted correctly or the structure was modified."
    assert "GET /health HTTP/1.1" in content, "Unrelated log lines were modified or removed."