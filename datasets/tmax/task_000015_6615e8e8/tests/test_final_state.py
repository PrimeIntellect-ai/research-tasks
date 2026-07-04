# test_final_state.py

import os
import json
import time
import subprocess
import pytest

def test_analyze_script_exists():
    assert os.path.isfile('/home/user/analyze.py'), "Script /home/user/analyze.py is missing."

def test_analyze_execution_and_accuracy():
    script_path = '/home/user/analyze.py'
    results_path = '/home/user/results.json'
    truth_path = '/app/ground_truth/reference.json'

    # Ensure truth file exists
    assert os.path.isfile(truth_path), f"Ground truth file {truth_path} is missing."

    # Remove existing results.json to ensure we are testing the script's actual output
    if os.path.exists(results_path):
        os.remove(results_path)

    start_time = time.time()
    try:
        subprocess.run(["python3", script_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {script_path} failed with error:\n{e.stderr}")
    elapsed = time.time() - start_time

    # Metric 2: Runtime speedup
    assert elapsed <= 2.0, f"Execution time {elapsed:.3f}s exceeds the 2.0s threshold."

    # Metric 1: Accuracy
    assert os.path.isfile(results_path), f"Output file {results_path} was not created."

    with open(results_path, 'r') as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {results_path} is not valid JSON.")

    with open(truth_path, 'r') as f:
        truth_data = json.load(f)

    assert agent_data == truth_data, "Accuracy must be 1.0. The generated results.json does not match the reference."

def test_query_api_modified():
    app_path = '/app/query_api/app.py'
    assert os.path.isfile(app_path), f"{app_path} is missing."

    with open(app_path, 'r') as f:
        content = f.read()

    # The task requires bypassing routes_cache and using a recursive CTE
    assert "routes_cache" not in content or "SELECT * FROM routes_cache" not in content, "Query API still appears to use the stale routes_cache."
    assert "RECURSIVE" in content.upper(), "Query API does not appear to use a RECURSIVE CTE as required."