# test_final_state.py
import os
import time
import subprocess
import json
import pytest

def test_output_file_exists_and_valid():
    """Check that the correct output file exists and contains valid JSON."""
    expected_file = "/home/user/release_14.5.2-beta.json"
    assert os.path.exists(expected_file), f"Output file {expected_file} missing. Did you extract the correct version from the image and run the script?"

    with open(expected_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {expected_file} is not valid JSON.")

def test_performance_metric():
    """Evaluate the execution time of the refactored script."""
    script_path = "/home/user/merge_builds.py"
    test_out = "/home/user/test_out.json"

    assert os.path.exists(script_path), f"Script {script_path} is missing."

    start = time.time()
    result = subprocess.run(["python3", script_path, test_out], capture_output=True, text=True)
    duration = time.time() - start

    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    assert duration <= 1.0, f"Script took {duration:.2f}s, which is slower than threshold 1.0s. Ensure the O(N^2) complexity was reduced."