# test_final_state.py

import os
import time
import json
import subprocess
import pytest

def test_rust_binary_performance_and_correctness():
    app_dir = "/app/graph-backup-analyzer"
    db_path = "/var/backups/graph_data.db"
    output_path = "/home/user/validation.json"
    golden_path = "/app/golden_validation.json"

    assert os.path.exists(app_dir), f"Directory {app_dir} does not exist."
    assert os.path.exists(db_path), f"Database {db_path} does not exist."
    assert os.path.exists(golden_path), f"Golden JSON {golden_path} does not exist."

    # Remove previous output if exists
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run the Rust binary and measure execution time
    start_time = time.time()
    result = subprocess.run(
        ["cargo", "run", "--release", "--", "--db", db_path, "--output", output_path],
        cwd=app_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    end_time = time.time()

    execution_time = end_time - start_time

    assert result.returncode == 0, f"Cargo run failed with code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    # Assert performance metric
    threshold = 2.0
    assert execution_time <= threshold, f"Execution time {execution_time:.2f}s exceeded the threshold of {threshold}s."

    # Assert correctness
    assert os.path.exists(output_path), f"Output file {output_path} was not generated."

    with open(output_path, 'r') as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_path} is not valid JSON.")

    with open(golden_path, 'r') as f:
        expected_json = json.load(f)

    # Order of matched paths might not be guaranteed, so we sort or compare elements
    # Assuming array of objects or lists. We can sort them as strings to compare
    def sort_json(data):
        if isinstance(data, list):
            return sorted([sort_json(x) for x in data], key=lambda x: str(x))
        elif isinstance(data, dict):
            return {k: sort_json(v) for k, v in data.items()}
        return data

    assert sort_json(actual_json) == sort_json(expected_json), "The generated JSON output does not match the expected golden JSON."