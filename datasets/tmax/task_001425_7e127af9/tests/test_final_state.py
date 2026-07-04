# test_final_state.py

import os
import subprocess
import pytest

def test_profiler_execution():
    """Test that the profiler script runs successfully with exit code 0."""
    script_path = "/home/user/profiler.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Profiler script failed to run. Stderr: {result.stderr}"
    assert "Total CPU processed:" in result.stdout, "Profiler script did not print the expected output."

def test_corrupt_files_log():
    """Test that the corrupt files log contains the correct filename."""
    log_path = "/home/user/corrupt_files.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read()

    assert "trace_542.json" in content, f"Expected 'trace_542.json' in {log_path}, but got: {content}"

def test_missing_keys_log():
    """Test that the missing keys log contains the correct filename."""
    log_path = "/home/user/missing_keys.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read()

    assert "trace_888.json" in content, f"Expected 'trace_888.json' in {log_path}, but got: {content}"