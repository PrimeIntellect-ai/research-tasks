# test_final_state.py

import os
import json
import time
import subprocess
import pytest

def test_etl_execution_time_and_output():
    script_path = "/home/user/etl_pipeline.py"
    output_path = "/home/user/top_users.json"

    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    # Remove output file if it exists to ensure we are testing the new run
    if os.path.exists(output_path):
        os.remove(output_path)

    start_time = time.time()
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    duration = time.time() - start_time

    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"
    assert duration <= 3.0, f"Execution took {duration:.2f}s, threshold is 3.0s"

    assert os.path.isfile(output_path), f"Output file not found at {output_path}"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} does not contain valid JSON.")

    assert isinstance(data, list), "Output JSON should be a list of objects."
    assert len(data) == 5, f"Expected exactly 5 users in output, got {len(data)}."

    for idx, item in enumerate(data):
        assert isinstance(item, dict), f"Item at index {idx} is not a dictionary."
        assert "user" in item, f"Item at index {idx} missing 'user' key."
        assert "out_degree" in item, f"Item at index {idx} missing 'out_degree' key."
        assert isinstance(item["user"], str), f"'user' at index {idx} should be a string."
        assert isinstance(item["out_degree"], int), f"'out_degree' at index {idx} should be an integer."

    # Check if they are sorted by out_degree descending (optional but good practice for top N)
    out_degrees = [item["out_degree"] for item in data]
    assert out_degrees == sorted(out_degrees, reverse=True), "The users are not sorted by out_degree in descending order."