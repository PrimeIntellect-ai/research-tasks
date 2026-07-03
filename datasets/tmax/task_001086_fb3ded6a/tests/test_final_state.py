# test_final_state.py

import os
import sys
import json
import time
import subprocess
import redis
import random
import pytest

def test_output_directory_and_acls():
    output_dir = "/home/user/output_data"
    assert os.path.isdir(output_dir), f"Directory {output_dir} does not exist."

    # Check ACLs
    res = subprocess.run(["getfacl", output_dir], capture_output=True, text=True)
    assert res.returncode == 0, "Failed to run getfacl."

    output = res.stdout
    assert "user:nobody:r-x" in output, f"ACL user:nobody:r-x not found in getfacl output:\n{output}"
    assert "default:user:nobody:r--" in output, f"Default ACL default:user:nobody:r-- not found in getfacl output:\n{output}"

def test_optimized_processor_exists():
    script_path = "/home/user/optimized_processor.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_processor_execution_and_metric():
    script_path = "/home/user/optimized_processor.py"
    output_file = "/home/user/output_data/processed.jsonl"

    # The script appends to the file, so we must remove it before timing the execution
    # to ensure we don't end up with more than 50,000 lines.
    if os.path.exists(output_file):
        os.remove(output_file)

    start = time.time()
    res = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    elapsed = time.time() - start

    assert res.returncode == 0, f"Script failed with exit code {res.returncode}. Stderr: {res.stderr}"
    assert elapsed <= 1.5, f"Metric threshold failed: Execution time {elapsed:.3f}s exceeded threshold of 1.5s."

    assert os.path.isfile(output_file), f"Output file {output_file} was not created."

    with open(output_file, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 50000, f"Expected 50000 lines in {output_file}, got {len(lines)}."

    # Verify data correctness
    try:
        r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
        r.ping()
    except redis.ConnectionError:
        pytest.fail("Could not connect to Redis on 127.0.0.1:6379 to verify data.")

    # Sample 100 random indices to verify data transformation accuracy
    indices = random.sample(range(50000), 100)
    for idx in indices:
        line = lines[idx].strip()
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {idx} in {output_file} is not valid JSON: {line}")

        assert "id" in data, f"Missing 'id' in output line {idx}: {data}"
        assert "processed_value" in data, f"Missing 'processed_value' in output line {idx}: {data}"

        sensor_id = data["id"]
        redis_data_str = r.get(sensor_id)
        assert redis_data_str is not None, f"Key {sensor_id} not found in Redis."

        redis_data = json.loads(redis_data_str)
        original_value = redis_data["value"]

        expected_value = original_value * 1.5
        actual_value = data["processed_value"]

        assert abs(actual_value - expected_value) < 1e-6, \
            f"Value mismatch for {sensor_id}: expected {expected_value}, got {actual_value}."