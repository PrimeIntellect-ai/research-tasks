# test_final_state.py

import os
import time
import subprocess
import pytest
import pandas as pd

def test_build_script_fixed():
    """Test that the build script no longer uses c++11 and uses c++17 or higher."""
    build_script_path = "/app/build.sh"
    assert os.path.isfile(build_script_path), f"Build script missing: {build_script_path}"

    with open(build_script_path, "r") as f:
        content = f.read()

    assert "-std=c++11" not in content, "Build script still contains the incorrect -std=c++11 flag."
    assert "-std=c++17" in content or "-std=c++20" in content or "-std=c++2a" in content, \
        "Build script must be updated to use -std=c++17 or higher."

def test_executable_exists():
    """Test that the C++ program was compiled to the correct location."""
    exe_path = "/home/user/log_analyzer"
    assert os.path.isfile(exe_path), f"Compiled executable missing: {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File is not executable: {exe_path}"

def test_performance_and_correctness():
    """Test the performance speedup and correctness of the C++ analyzer."""
    log_file = "/home/user/server_logs.jsonl"
    baseline_script = "/app/baseline.py"
    ref_csv = "/tmp/ref.csv"
    agent_exe = "/home/user/log_analyzer"
    agent_csv = "/home/user/summary.csv"

    assert os.path.isfile(log_file), f"Log file missing: {log_file}"
    assert os.path.isfile(baseline_script), f"Baseline script missing: {baseline_script}"

    # Measure Baseline Time
    start_time = time.time()
    try:
        subprocess.run(
            ["python3", baseline_script, log_file, ref_csv],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Baseline script failed to execute. Stderr: {e.stderr}")
    base_time = time.time() - start_time

    assert os.path.isfile(ref_csv), f"Baseline output CSV missing: {ref_csv}"

    # Ensure the agent's summary.csv is removed before running to verify it creates it
    if os.path.exists(agent_csv):
        os.remove(agent_csv)

    # Measure C++ Time
    start_time = time.time()
    try:
        subprocess.run(
            [agent_exe],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent C++ executable failed. Stderr: {e.stderr}")
    cpp_time = time.time() - start_time

    assert os.path.isfile(agent_csv), f"Agent output CSV missing: {agent_csv}"

    # Verify Correctness
    ref_df = pd.read_csv(ref_csv).set_index('endpoint')
    out_df = pd.read_csv(agent_csv).set_index('endpoint')

    assert out_df.index.equals(ref_df.index), "The endpoints (index) in the output CSV do not match the baseline."

    count_diff = (out_df['count'] != ref_df['count']).sum()
    assert count_diff == 0, f"Count mismatch for {count_diff} endpoints."

    avg_latency_diff = (out_df['avg_latency'] - ref_df['avg_latency']).abs().max()
    assert avg_latency_diff < 0.001, f"Average latency mismatch. Max diff: {avg_latency_diff:.5f} (threshold 0.001)"

    max_latency_diff = (out_df['max_latency'] - ref_df['max_latency']).abs().max()
    assert max_latency_diff < 0.001, f"Max latency mismatch. Max diff: {max_latency_diff:.5f} (threshold 0.001)"

    # Verify Speedup
    speedup = base_time / cpp_time
    assert speedup >= 5.0, f"Speedup is {speedup:.2f}x (Baseline: {base_time:.3f}s, C++: {cpp_time:.3f}s), threshold is 5.0x"