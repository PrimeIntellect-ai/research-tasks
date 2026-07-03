# test_final_state.py

import os
import subprocess
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/evaluate_perf.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_script_output():
    script_path = "/home/user/evaluate_perf.sh"

    try:
        result = subprocess.run([script_path], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed with exit code {e.returncode}. Stderr: {e.stderr}")

    output = result.stdout.strip().split('\n')

    expected_output = [
        "Baseline p99: 45.15",
        "New p99: 70.13",
        "Wasserstein: 5.42",
        "Regression: YES"
    ]

    assert len(output) == 4, f"Expected 4 lines of output, got {len(output)}: {output}"

    for i, (actual, expected) in enumerate(zip(output, expected_output)):
        assert actual.strip() == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual.strip()}'"