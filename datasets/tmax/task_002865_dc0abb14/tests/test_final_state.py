# test_final_state.py

import os
import re
import subprocess
import pytest

def test_run_analysis_script_exists_and_executable():
    """Verify that the user created the run_analysis.sh script and made it executable."""
    script_path = "/home/user/run_analysis.sh"
    assert os.path.isfile(script_path), f"Missing analysis script at {script_path}"
    assert os.access(script_path, os.X_OK), f"Analysis script at {script_path} is not executable. Did you run chmod +x?"

def test_interceptor_build_success():
    """Verify that the interceptor was successfully built."""
    so_path = "/home/user/interceptor/hook.so"
    assert os.path.isfile(so_path), f"Missing compiled interceptor at {so_path}. The build.sh script may have failed or was not run."

def test_key_extraction_metric():
    """
    Run the user's analysis script and evaluate the extraction success rate.
    The metric is the ratio of unique, valid 32-character hex strings to 100.
    Threshold is >= 0.95.
    """
    script_path = "/home/user/run_analysis.sh"
    keys_file = "/home/user/extracted_keys.txt"

    # Execute the user's script to perform the extraction
    try:
        subprocess.run([script_path], check=True, timeout=300, capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {script_path} timed out after 300 seconds. Check for infinite loops in your retry logic.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {script_path} failed with return code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")

    # Verify the output file exists
    assert os.path.isfile(keys_file), f"Output file {keys_file} was not created by the analysis script."

    # Read and parse the extracted keys
    with open(keys_file, 'r') as f:
        content = f.read().splitlines()

    valid_keys = set()
    for line in content:
        line = line.strip()
        # Check for exactly 32 hex characters
        if re.match(r'^[a-fA-F0-9]{32}$', line):
            valid_keys.add(line)

    # Calculate the metric
    expected_keys = 100
    score = len(valid_keys) / float(expected_keys)
    threshold = 0.95

    # Assert against the threshold with a clear message
    assert score >= threshold, (
        f"Extraction success rate is below the required threshold.\n"
        f"Metric (score): {score}\n"
        f"Threshold: >= {threshold}\n"
        f"Found {len(valid_keys)} unique, valid keys out of {expected_keys} expected."
    )