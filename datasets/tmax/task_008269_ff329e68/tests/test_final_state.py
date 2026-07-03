# test_final_state.py

import os
import pytest

def test_crash_input_content():
    """Verify that crash_input.txt contains the exact extracted payload."""
    expected_payload = '{"op": "multiply", "args": [18446744073709551616, 55'
    file_path = "/home/user/crash_input.txt"

    assert os.path.exists(file_path), f"File {file_path} does not exist."
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == expected_payload, f"Content of {file_path} is incorrect. Expected '{expected_payload}', got '{content}'."

def test_mre_go_exists_and_looks_valid():
    """Verify that mre.go exists and contains necessary Go code elements."""
    file_path = "/home/user/mre.go"

    assert os.path.exists(file_path), f"Go program {file_path} does not exist."
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "package main" in content, "mre.go does not contain 'package main'."
    assert "MathRequest" in content, "mre.go does not define the MathRequest struct."
    assert "json.Unmarshal" in content or "json.NewDecoder" in content, "mre.go does not seem to use json unmarshaling."
    assert "crash_input.txt" in content, "mre.go does not reference the crash_input.txt file."

def test_diagnostic_log_content():
    """Verify that diagnostic.log contains the expected json unmarshal error."""
    file_path = "/home/user/diagnostic.log"

    assert os.path.exists(file_path), f"Log file {file_path} does not exist."
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content, f"{file_path} is empty."

    # The error should be about unexpected EOF or unmarshaling the large number.
    valid_errors = [
        "unexpected end of JSON input",
        "json: cannot unmarshal number",
        "unexpected EOF"
    ]

    assert any(err in content for err in valid_errors), (
        f"diagnostic.log does not contain a recognized JSON unmarshal error. "
        f"Content was: '{content}'"
    )