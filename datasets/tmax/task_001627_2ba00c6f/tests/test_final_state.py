# test_final_state.py
import os
import json
import time
import subprocess
import pytest

def test_pipeline_execution_and_metric():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.exists(script_path), f"Wrapper script not found: {script_path}"

    # Clear old results to ensure we are testing the current run
    results_file = '/tmp/validator_results.json'
    try:
        with open(results_file, 'w') as f:
            json.dump({}, f)
    except Exception:
        pass

    start_time = time.time()
    res = subprocess.run(["bash", script_path], capture_output=True, text=True)
    end_time = time.time()

    runtime_seconds = end_time - start_time

    assert res.returncode == 0, f"Pipeline returned non-zero exit code {res.returncode}. Stderr: {res.stderr}\nStdout: {res.stdout}"

    assert os.path.exists(results_file), f"Results file not found: {results_file}. Did the validation service write it?"

    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
    except Exception as e:
        pytest.fail(f"Could not read validator results: {e}")

    assert len(results) >= 10, f"Processed too few frames: {len(results)}. Expected at least 10 frames to be submitted."

    # Check the metric threshold
    assert runtime_seconds <= 3.0, f"Execution time {runtime_seconds:.3f}s exceeded the threshold of 3.0s."