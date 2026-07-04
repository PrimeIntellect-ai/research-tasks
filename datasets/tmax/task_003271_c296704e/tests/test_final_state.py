# test_final_state.py

import os
import json
import time
import math
import sqlite3
import subprocess
import pytest

def get_golden_results(db_path):
    """Compute the expected results based on the corrected logic."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT n1.region, SUM(e.weight * n2.value)
    FROM nodes n1
    JOIN edges e ON n1.id = e.source
    JOIN nodes n2 ON e.target = n2.id
    WHERE n1.type != 'bot' AND n1.value > 10
      AND n2.type != 'bot'
    GROUP BY n1.region
    """

    cursor.execute(query)
    results = {}
    for row in cursor.fetchall():
        region, total = row
        results[region] = total

    conn.close()
    return results

def test_optimized_script_exists():
    assert os.path.isfile("/app/optimized.py"), "/app/optimized.py is missing"

def test_results_json_correctness():
    assert os.path.isfile("/app/results.json"), "/app/results.json is missing"

    with open("/app/results.json", "r") as f:
        opt_res = json.load(f)

    golden_res = get_golden_results("/app/network.db")

    # Check keys
    assert set(opt_res.keys()) == set(golden_res.keys()), "The regions in results.json do not match the expected regions."

    # Check values with float tolerance
    for region, expected_val in golden_res.items():
        actual_val = opt_res[region]
        assert math.isclose(actual_val, expected_val, rel_tol=1e-5), \
            f"Value for region {region} is incorrect. Expected ~{expected_val}, got {actual_val}"

def test_performance_speedup():
    """Measure the execution time of the optimized script and ensure speedup >= 15.0."""
    # Run optimized script
    start_time = time.time()
    result = subprocess.run(
        ["python3", "/app/optimized.py"],
        capture_output=True,
        text=True
    )
    opt_time = time.time() - start_time

    assert result.returncode == 0, f"optimized.py failed to execute:\n{result.stderr}"

    # Baseline time is assumed to be ~2.5 seconds based on the prompt
    baseline_time = 2.5
    speedup = baseline_time / opt_time if opt_time > 0 else float('inf')

    assert speedup >= 15.0, f"Speedup too low. Baseline: {baseline_time}s, Optimized: {opt_time:.4f}s, Speedup: {speedup:.2f}x (Threshold: 15.0x)"