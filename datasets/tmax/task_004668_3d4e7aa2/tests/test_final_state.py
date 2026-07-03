# test_final_state.py

import os
import subprocess
import time
import pytest

def test_optimized_files_exist():
    assert os.path.exists('/home/user/projected_graph.tsv'), "Optimized graph file '/home/user/projected_graph.tsv' is missing."
    assert os.path.isfile('/home/user/projected_graph.tsv'), "'/home/user/projected_graph.tsv' should be a file."

    assert os.path.exists('/home/user/fast_query.txt'), "Optimized query file '/home/user/fast_query.txt' is missing."
    assert os.path.isfile('/home/user/fast_query.txt'), "'/home/user/fast_query.txt' should be a file."

def test_performance_and_correctness():
    # 1. Run baseline query to get the true expected count
    baseline_cmd = ['/app/pattern_matcher', '/home/user/raw_graph.tsv', '/home/user/slow_query.txt']
    res_baseline = subprocess.run(baseline_cmd, capture_output=True, text=True)
    assert res_baseline.returncode == 0, f"Baseline query failed to run. stderr: {res_baseline.stderr}"

    baseline_matches = None
    for line in res_baseline.stdout.splitlines():
        if line.startswith("Matches:"):
            baseline_matches = line.strip()
            break
    assert baseline_matches is not None, "Could not find 'Matches: X' in baseline output."

    # 2. Run the optimized query and measure execution time
    fast_cmd = ['/app/pattern_matcher', '/home/user/projected_graph.tsv', '/home/user/fast_query.txt']
    start_time = time.time()
    try:
        res_fast = subprocess.run(fast_cmd, capture_output=True, text=True, timeout=5.0)
    except subprocess.TimeoutExpired:
        pytest.fail("Fast query took longer than 5.0 seconds (timeout). Expected <= 0.5s.")

    elapsed = time.time() - start_time

    assert res_fast.returncode == 0, f"Fast query failed to run. stderr: {res_fast.stderr}"

    fast_matches = None
    for line in res_fast.stdout.splitlines():
        if line.startswith("Matches:"):
            fast_matches = line.strip()
            break

    # 3. Assert correctness
    assert fast_matches == baseline_matches, f"Incorrect result. Expected '{baseline_matches}', got '{fast_matches}'."

    # 4. Assert performance metric
    assert elapsed <= 0.5, f"Execution time {elapsed:.3f}s exceeds threshold of 0.5s."