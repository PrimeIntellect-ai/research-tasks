# test_final_state.py

import os
import subprocess
import pytest

def test_trigger_txt():
    path = "/home/user/trigger.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "31337", f"Expected trigger.txt to contain '31337', but got '{content}'"

def test_process_logs_execution():
    script_path = "/home/user/process_logs.py"
    assert os.path.exists(script_path), f"File {script_path} does not exist."

    # Run the script
    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )

    # Check exit code
    assert result.returncode == 0, f"process_logs.py exited with code {result.returncode}. Stderr: {result.stderr}"

    # Check stdout
    stdout_stripped = result.stdout.strip()
    assert stdout_stripped == "CORRUPTION_DETECTED", f"Expected stdout to be 'CORRUPTION_DETECTED', but got '{stdout_stripped}'"

def test_aggregate_txt():
    path = "/home/user/aggregate.txt"
    assert os.path.exists(path), f"File {path} does not exist. process_logs.py might not have created it."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "600", f"Expected aggregate.txt to contain '600', but got '{content}'"