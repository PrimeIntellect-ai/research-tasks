# test_final_state.py

import os
import stat
import subprocess
import pytest

def compute_xor_hex(text: str, key: int) -> str:
    """Helper to compute the expected XOR hex string."""
    return "".join(f"{ord(c) ^ key:02x}" for c in text)

def test_generate_payload_script_exists_and_executable():
    script_path = "/home/user/generate_payload.sh"

    assert os.path.exists(script_path), f"The script {script_path} is missing."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

    st = os.stat(script_path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"The script {script_path} is not executable. Please run 'chmod +x {script_path}'."

def test_generate_payload_script_functionality():
    script_path = "/home/user/generate_payload.sh"

    if not os.path.exists(script_path) or not os.access(script_path, os.X_OK):
        pytest.fail(f"Cannot test functionality because {script_path} is missing or not executable.")

    # We test the script with a generic string to ensure it actually performs the cryptography
    # and doesn't just hardcode the final answer.
    test_string = "Test_String_123"
    key = 0x4B
    expected_hex = compute_xor_hex(test_string, key)

    try:
        result = subprocess.run([script_path, test_string], capture_output=True, text=True, check=False)
    except Exception as e:
        pytest.fail(f"Failed to execute {script_path}: {e}")

    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr.strip()}"

    output = result.stdout.strip().lower()
    assert output == expected_hex, (
        f"Script did not produce the correct XOR hex output for input '{test_string}'. "
        f"Expected '{expected_hex}', but got '{output}'."
    )

def test_final_payload_file():
    payload_path = "/home/user/final_payload.txt"

    assert os.path.exists(payload_path), f"The final payload file {payload_path} is missing."
    assert os.path.isfile(payload_path), f"The path {payload_path} is not a regular file."

    with open(payload_path, "r") as f:
        content = f.read().strip().lower()

    target_string = "EXPLOIT_SANDBOX_ESCALATE_PID_1"
    key = 0x4B
    expected_hex = compute_xor_hex(target_string, key)

    assert content == expected_hex, (
        f"The contents of {payload_path} do not match the expected encrypted payload for '{target_string}'. "
        f"Expected '{expected_hex}', but got '{content}'."
    )