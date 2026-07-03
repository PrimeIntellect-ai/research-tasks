# test_final_state.py
import os
import time
import subprocess
import pandas as pd
import pytest

def run_cmd(cmd):
    start = time.time()
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return time.time() - start

def test_fast_graph_exists_and_executable():
    binary_path = "/home/user/fast_graph"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} not found. Did you compile your C program?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_speedup_and_correctness():
    legacy_output = "/home/user/legacy_output.csv"
    agent_output = "/home/user/results.csv"

    # Remove outputs if they exist to ensure fresh run
    if os.path.exists(legacy_output):
        os.remove(legacy_output)
    if os.path.exists(agent_output):
        os.remove(agent_output)

    # Run legacy calc
    time_legacy = run_cmd(f"/app/legacy_calc > {legacy_output}")
    assert os.path.isfile(legacy_output), "Legacy output was not created."

    # Run agent calc
    time_agent = run_cmd("/home/user/fast_graph")
    time_agent = max(time_agent, 1e-6)  # Prevent division by zero

    assert os.path.isfile(agent_output), f"Agent output {agent_output} was not created."

    # Compare correctness
    try:
        df_legacy = pd.read_csv(legacy_output, header=None)
    except pd.errors.EmptyDataError:
        pytest.fail("Legacy output is empty.")

    try:
        df_agent = pd.read_csv(agent_output, header=None)
    except pd.errors.EmptyDataError:
        pytest.fail("Agent output is empty.")

    # The format is category_group,id,total_weight,rank
    # Sort by category_group (0) and rank (3)
    df_legacy_sorted = df_legacy.sort_values([0, 3, 1]).reset_index(drop=True)
    df_agent_sorted = df_agent.sort_values([0, 3, 1]).reset_index(drop=True)

    try:
        pd.testing.assert_frame_equal(
            df_legacy_sorted, 
            df_agent_sorted,
            check_dtype=False,
            check_exact=False,
            rtol=1e-4
        )
    except AssertionError as e:
        pytest.fail(f"Agent output does not match legacy output exactly:\n{e}")

    # Calculate speedup
    speedup = time_legacy / time_agent
    assert speedup >= 25.0, f"Speedup too low: {speedup:.2f}x (Legacy: {time_legacy:.4f}s, Agent: {time_agent:.4f}s). Target is >= 25.0x."