# test_final_state.py

import os
import subprocess
import time
import pandas as pd
import pytest

def run_and_time(cmd, cwd):
    start = time.time()
    try:
        subprocess.run(cmd, check=True, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Command {cmd} failed in {cwd}: {e}")
    return time.time() - start

def test_agent_binary_exists():
    agent_bin = "/home/user/fast_query"
    assert os.path.exists(agent_bin), f"Agent binary {agent_bin} does not exist. Did you compile it?"
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable."

def test_correctness():
    ref_cmd = ['/app/ref_engine']
    agent_cmd = ['/home/user/fast_query']

    # Run reference engine to generate truth
    try:
        subprocess.run(ref_cmd, cwd='/app/data', check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pytest.fail("Reference engine failed to run.")

    ref_results_path = '/app/data/results.csv'
    assert os.path.exists(ref_results_path), "Reference engine did not produce results.csv"
    ref_df = pd.read_csv(ref_results_path)

    # Run agent engine
    try:
        subprocess.run(agent_cmd, cwd='/home/user', check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pytest.fail("Agent fast_query failed to run.")

    agent_results_path = '/home/user/results.csv'
    assert os.path.exists(agent_results_path), f"Agent did not produce {agent_results_path}"
    agent_df = pd.read_csv(agent_results_path)

    # Check exact match
    ref_sorted = ref_df.sort_values(by=['Product', 'User1', 'User2']).reset_index(drop=True)
    agent_sorted = agent_df.sort_values(by=['Product', 'User1', 'User2']).reset_index(drop=True)

    try:
        pd.testing.assert_frame_equal(ref_sorted, agent_sorted)
    except AssertionError as e:
        pytest.fail(f"Agent results.csv does not match reference output:\n{e}")

def test_speedup():
    ref_cmd = ['/app/ref_engine']
    agent_cmd = ['/home/user/fast_query']

    # Measure speedup (average of 3 runs)
    t_ref = sum(run_and_time(ref_cmd, cwd='/app/data') for _ in range(3)) / 3.0
    t_agent = sum(run_and_time(agent_cmd, cwd='/home/user') for _ in range(3)) / 3.0

    speedup = t_ref / t_agent

    assert speedup >= 10.0, (
        f"Speedup is {speedup:.2f}x, which is less than the required 10.0x threshold. "
        f"(Reference time: {t_ref:.4f}s, Agent time: {t_agent:.4f}s)"
    )