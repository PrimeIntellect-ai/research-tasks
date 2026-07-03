# test_final_state.py

import os
import pytest

def test_redactor_c_exists_and_seccomp():
    """Test that /home/user/redactor.c exists and contains strict seccomp setup."""
    file_path = "/home/user/redactor.c"
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    assert "PR_SET_SECCOMP" in content, "PR_SET_SECCOMP not found in redactor.c"
    assert "SECCOMP_MODE_STRICT" in content, "SECCOMP_MODE_STRICT not found in redactor.c"

def test_redactor_executable_exists():
    """Test that the compiled executable /home/user/redactor exists and is executable."""
    file_path = "/home/user/redactor"
    assert os.path.isfile(file_path), f"{file_path} does not exist."
    assert os.access(file_path, os.X_OK), f"{file_path} is not executable."

def test_safe_logs_content():
    """Test that /home/user/safe_logs.txt exists and has the correctly redacted content."""
    file_path = "/home/user/safe_logs.txt"
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    expected_content = """[INFO] Server started on port 8080.
[DEBUG] User authentication attempt.
[WARN] Deprecated auth token found: [REDACTED]
[INFO] Authentication successful.
[DEBUG] Payload metadata: <SECRET:001122334455>
[WARN] Deprecated auth token found: [REDACTED]
[INFO] Connection closed.
"""

    with open(file_path, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), f"Content of {file_path} does not match expected output exactly."