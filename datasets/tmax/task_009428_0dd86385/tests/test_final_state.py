# test_final_state.py

import os
import subprocess
import pytest

def test_api_key_recovered():
    api_key_path = "/home/user/api_key.txt"
    assert os.path.isfile(api_key_path), f"{api_key_path} does not exist"

    with open(api_key_path, "r") as f:
        content = f.read().strip()

    expected_key = "sk_live_8f7d6c5b4a392817"
    assert content == expected_key, f"API key recovered is incorrect. Expected {expected_key}, got {content}"

def test_output_file_correct():
    output_path = "/home/user/output.txt"
    assert os.path.isfile(output_path), f"{output_path} does not exist"

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) > 0, f"{output_path} is empty"

    expected_line = "Total bytes: 10000000000000000000"
    assert lines[-1] == expected_line, f"Final output line is incorrect. Expected '{expected_line}', got '{lines[-1]}'"

def test_script_execution():
    script_path = "/home/user/backup_repo/backup_manager.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

    try:
        # Run the script with a timeout to ensure it doesn't infinite loop
        result = subprocess.run(
            [script_path],
            capture_output=True,
            text=True,
            timeout=5,
            check=True
        )
        lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        assert len(lines) > 0, "Script produced no output"
        expected_line = "Total bytes: 10000000000000000000"
        assert lines[-1] == expected_line, f"Script output is incorrect. Expected '{expected_line}', got '{lines[-1]}'"

    except subprocess.TimeoutExpired:
        pytest.fail("Script timed out, indicating the infinite loop was not fixed.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script failed with error: {e.stderr}")

def test_script_uses_bc_or_awk():
    script_path = "/home/user/backup_repo/backup_manager.sh"
    with open(script_path, "r") as f:
        content = f.read()

    assert "bc" in content or "awk" in content, "Script must use 'bc' or 'awk' to fix numerical instability."