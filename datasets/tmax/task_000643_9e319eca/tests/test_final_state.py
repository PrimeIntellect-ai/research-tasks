# test_final_state.py

import os
import time
import json
import subprocess
import sys
import pytest

def test_fast_calc_correctness_and_performance():
    script_path = '/home/user/fast_calc.py'
    output_path = '/home/user/roots_summary.json'
    expected_path = '/tmp/expected_roots.json'

    assert os.path.isfile(script_path), f"Script missing at {script_path}"
    assert os.path.isfile(expected_path), f"Expected roots JSON missing at {expected_path}"

    with open(expected_path, 'r') as f:
        expected = json.load(f)

    # Remove previous output if exists to ensure we are testing the script's execution
    if os.path.exists(output_path):
        os.remove(output_path)

    start_time = time.time()
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    elapsed = time.time() - start_time

    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    assert os.path.isfile(output_path), f"Script did not produce the expected output file at {output_path}"

    try:
        with open(output_path, 'r') as f:
            actual = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read or parse {output_path}: {e}")

    assert actual == expected, "The computed cumulative sizes in roots_summary.json do not match the expected results."

    # Assert performance
    threshold = 1.0
    assert elapsed <= threshold, f"Execution time {elapsed:.4f}s exceeded the threshold of {threshold}s. The script is not optimized enough."