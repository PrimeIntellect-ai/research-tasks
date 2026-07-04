# test_final_state.py

import os
import json
import subprocess
import pytest

def test_rust_api_compiles():
    """Verify that the Rust API compiles successfully after the borrow checker fix."""
    api_dir = "/home/user/session-api"
    assert os.path.isdir(api_dir), f"Directory {api_dir} does not exist."

    # Run cargo check to ensure it compiles
    try:
        result = subprocess.run(
            ["cargo", "check"],
            cwd=api_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"Rust project failed to compile:\n{result.stderr}"
    except FileNotFoundError:
        # Fallback if cargo is not in PATH for the test runner, check the source file directly
        main_rs_path = os.path.join(api_dir, "src/main.rs")
        with open(main_rs_path, "r") as f:
            content = f.read()
        assert "let result = process_token(token_ref);" not in content, \
            "The borrow checker error in src/main.rs has not been fixed."

def test_pbt_script_exists():
    """Verify the Bash property-based tester script exists."""
    script_path = "/home/user/pbt.sh"
    assert os.path.isfile(script_path), f"Fuzzer script {script_path} does not exist."

def test_bug_report_exists_and_format():
    """Verify the bug report exists, is a single line, and contains valid JSON."""
    log_path = "/home/user/bug_report.log"
    assert os.path.isfile(log_path), f"Bug report {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "Bug report is empty."
    assert len(lines) == 1, "Bug report must contain exactly one line with the raw JSON string."

    content = lines[0].strip()
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail("Bug report does not contain a valid JSON string.")

    assert data.get("request_type") == "validate", "JSON missing or incorrect 'request_type'."
    assert "payload" in data, "JSON missing 'payload' object."

    payload = data["payload"]
    assert "token" in payload, "Payload missing 'token'."
    assert "metadata" in payload, "Payload missing 'metadata'."
    assert "len" in payload["metadata"], "Metadata missing 'len'."

def test_bug_report_token_triggers_crash():
    """Verify the token in the bug report actually triggers the hidden Rust panic."""
    log_path = "/home/user/bug_report.log"
    assert os.path.isfile(log_path), f"Bug report {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    data = json.loads(content)
    token = data["payload"]["token"]

    # Replicate the Rust logic to verify the crash condition
    # Condition: Exactly 3 consecutive uppercase ASCII letters followed by an ASCII digit.
    upper_count = 0
    crashed = False
    for c in token:
        if c.isupper() and c.isascii():
            upper_count += 1
        elif c.isdigit() and c.isascii() and upper_count == 3:
            crashed = True
            break
        else:
            upper_count = 0

    assert crashed, (
        f"The token '{token}' found in the bug report does not trigger the API panic. "
        "It must contain exactly three consecutive uppercase letters followed immediately by a digit."
    )