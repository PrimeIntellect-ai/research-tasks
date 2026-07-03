# test_final_state.py

import os
import subprocess
import pytest

def test_start_script_fixed():
    """Verify that start.sh has been fixed and executes successfully."""
    script_path = "/home/user/bin/start.sh"
    assert os.path.isfile(script_path), f"Start script {script_path} is missing."

    # Run the script and check the return code
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {script_path} failed with exit code {result.returncode}. Output: {result.stderr}"

def test_processed_txt_contents():
    """Verify that processed.txt contains the correct decrypted message."""
    processed_path = "/home/user/data/processed.txt"
    assert os.path.isfile(processed_path), f"Decrypted output file {processed_path} is missing."

    with open(processed_path, "r") as f:
        content = f.read().strip()

    expected_message = "CRITICAL_TELEMETRY_RECOVERED_SUCCESSFULLY_9921"
    assert expected_message in content, f"{processed_path} does not contain the expected decrypted message."

def test_resolution_txt_contents():
    """Verify that resolution.txt contains exactly the key and the decrypted message."""
    resolution_path = "/home/user/resolution.txt"
    assert os.path.isfile(resolution_path), f"Resolution file {resolution_path} is missing."

    with open(resolution_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"{resolution_path} should contain exactly 2 non-empty lines, found {len(lines)}."

    expected_key = "b7f9a2d4"
    expected_message = "CRITICAL_TELEMETRY_RECOVERED_SUCCESSFULLY_9921"

    assert lines[0] == expected_key, f"First line of {resolution_path} is incorrect. Expected '{expected_key}', got '{lines[0]}'."
    assert lines[1] == expected_message, f"Second line of {resolution_path} is incorrect. Expected '{expected_message}', got '{lines[1]}'."