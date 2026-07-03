# test_final_state.py
import os
import json
import time
import subprocess
import random
import pytest

def test_local_correctness():
    """Check if the output file for the sample data exists and contains the correct cycle."""
    assert os.path.exists("/app/cycle.json"), "Missing /app/cycle.json. Did you run the binary on /app/locks.csv?"

    try:
        with open("/app/cycle.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to parse /app/cycle.json: {e}")

    expected = ["TX_88192", "TX_11111", "TX_22222", "TX_33333"]
    assert data == expected, f"Incorrect cycle found on sample data. Expected {expected}, got {data}"

def test_hidden_dataset_performance():
    """Verify performance and correctness on a 2-million edge hidden graph."""
    binary_path = "/home/user/deadlock_analyzer/target/release/deadlock_analyzer"
    assert os.path.exists(binary_path), f"Release binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

    hidden_csv = "/tmp/hidden_locks.csv"
    hidden_out = "/tmp/hidden_out.json"

    # Generate hidden dataset (2 million edges)
    # We use IDs from 100000 to 999999 to ensure we don't accidentally create a shorter cycle for TX_99999
    with open(hidden_csv, 'w') as f:
        for _ in range(200):
            chunk = []
            for _ in range(10000):
                w = f"TX_{random.randint(100000, 999999)}"
                h = f"TX_{random.randint(100000, 999999)}"
                chunk.append(f"{w},{h},1690000000\n")
            f.writelines(chunk)

        # Add the known shortest cycle
        cycle = ["TX_99999", "TX_A", "TX_B", "TX_C", "TX_D"]
        for i in range(len(cycle)):
            f.write(f"{cycle[i]},{cycle[(i+1)%len(cycle)]},1690000000\n")

    # Run benchmark
    start_time = time.time()
    res = subprocess.run([binary_path, hidden_csv, "TX_99999", hidden_out], capture_output=True, text=True)
    end_time = time.time()

    assert res.returncode == 0, f"Binary execution failed with code {res.returncode}. Stderr: {res.stderr}"

    runtime = end_time - start_time

    assert os.path.exists(hidden_out), f"Hidden output JSON not generated at {hidden_out}"
    try:
        with open(hidden_out, "r") as f:
            hidden_data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to parse {hidden_out}: {e}")

    expected_cycle = ["TX_99999", "TX_A", "TX_B", "TX_C", "TX_D"]
    assert hidden_data == expected_cycle, f"Incorrect cycle on hidden data. Expected {expected_cycle}, got {hidden_data}"

    assert runtime < 0.5, f"Execution time {runtime:.3f}s exceeded threshold of 0.5s"