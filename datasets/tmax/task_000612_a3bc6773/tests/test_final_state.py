# test_final_state.py

import os
import json
import time
import subprocess

def test_libfastmerge_compiled():
    """Verify that the shared library was compiled successfully."""
    so_path = "/app/libfastmerge/libfastmerge.so"
    assert os.path.exists(so_path), f"{so_path} was not generated. Check the Makefile fixes."

def test_organizer_compiled():
    """Verify that the C++ organizer binary exists and is executable."""
    bin_path = "/home/user/organizer"
    assert os.path.exists(bin_path), f"{bin_path} binary is missing. Did you compile organizer.cpp?"
    assert os.access(bin_path, os.X_OK), f"{bin_path} is not executable."

def test_execution_time_and_correctness():
    """Verify the metric threshold (runtime <= 2.0s) and the correctness of the output."""
    results_file = "/home/user/results.jsonl"

    # Remove results.jsonl if it exists to ensure we measure a fresh run
    if os.path.exists(results_file):
        os.remove(results_file)

    env = os.environ.copy()
    # Ensure the shared library can be found
    if "LD_LIBRARY_PATH" in env:
        env["LD_LIBRARY_PATH"] = "/app/libfastmerge:" + env["LD_LIBRARY_PATH"]
    else:
        env["LD_LIBRARY_PATH"] = "/app/libfastmerge"

    start = time.time()
    res = subprocess.run(
        ["/home/user/organizer"], 
        env=env, 
        capture_output=True
    )
    end = time.time()

    assert res.returncode == 0, f"Organizer failed with return code {res.returncode}. stderr: {res.stderr.decode('utf-8', errors='ignore')}"

    runtime = end - start

    assert os.path.exists(results_file), f"{results_file} was not created by the organizer."

    with open(results_file, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 10000, f"Expected 10000 results in {results_file}, got {len(lines)}. Ensure all requests are processed."

    # Validate the JSON schema on a sample of lines
    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Invalid JSON on line {i+1} in results.jsonl: {line}"

        assert "job_id" in data, f"Missing 'job_id' on line {i+1}"
        assert "status" in data, f"Missing 'status' on line {i+1}"
        assert data["status"] in ["success", "invalid"], f"Invalid status '{data['status']}' on line {i+1}"
        assert "merged_length" in data, f"Missing 'merged_length' on line {i+1}"
        assert isinstance(data["merged_length"], int), f"'merged_length' must be an integer on line {i+1}"
        assert isinstance(data["job_id"], int), f"'job_id' must be an integer on line {i+1}"

    # Finally, assert the performance metric
    assert runtime <= 2.0, f"Execution time {runtime:.3f}s exceeded threshold of 2.0s. Ensure your C++ implementation is highly concurrent."