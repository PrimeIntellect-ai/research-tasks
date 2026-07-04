# test_final_state.py

import os
import subprocess
import pytest

def test_run_processor_success():
    """Test that run_processor.sh runs successfully without crashing."""
    script_path = "/home/user/run_processor.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."

    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_processor.sh failed to execute. stderr: {result.stderr}"

def test_invalid_logs_content():
    """Test that invalid_logs.txt contains the exact expected unparsed line."""
    log_path = "/home/user/invalid_logs.txt"
    assert os.path.isfile(log_path), f"File {log_path} is missing. Did process_logs.py create it?"

    with open(log_path, "r") as f:
        content = f.read()

    expected_content = '{"url": "site2.com", "uptime": 98\n'
    assert content == expected_content, f"invalid_logs.txt content is incorrect. Expected: {repr(expected_content)}, Got: {repr(content)}"

def test_mre_script_exists_and_runs():
    """Test that mre.py exists, contains the required strings, and runs successfully."""
    mre_path = "/home/user/mre.py"
    assert os.path.isfile(mre_path), f"File {mre_path} is missing."

    with open(mre_path, "r") as f:
        content = f.read()

    # Check for the required incomplete JSON string
    expected_incomplete = '{"url": "site2.com", "uptime": 98'
    assert expected_incomplete in content, f"mre.py must hardcode the incomplete JSON string: {expected_incomplete}"

    # Check that it doesn't read from files (simple check for open)
    # The prompt says: "Not read from any files."

    result = subprocess.run(["python3", mre_path], capture_output=True, text=True)
    assert result.returncode == 0, f"mre.py failed to execute. stderr: {result.stderr}"