# test_final_state.py

import os
import time
import subprocess
import pandas as pd
import pytest

def test_files_exist():
    assert os.path.isfile("/home/user/fast_mcmc.cpp"), "/home/user/fast_mcmc.cpp does not exist"
    assert os.path.isfile("/home/user/workflow.ipynb"), "/home/user/workflow.ipynb does not exist"

def test_performance_and_accuracy():
    cpp_file = "/home/user/fast_mcmc.cpp"
    executable = "/tmp/fast_mcmc"
    data_file = "/app/data.csv"
    oracle_binary = "/app/oracle_mcmc"
    oracle_output = "/tmp/oracle_samples.csv"
    agent_output = "/tmp/fast_samples.csv"

    # Compile the agent's C++ code
    compile_cmd = ["g++", "-O3", "-fopenmp", cpp_file, "-o", executable]
    try:
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Compilation failed:\n{e.stderr}")

    assert os.path.isfile(executable), "Agent executable was not generated"

    # Run Oracle
    start_oracle = time.time()
    try:
        subprocess.run([oracle_binary, data_file, oracle_output], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle binary failed to run:\n{e.stderr}")
    oracle_time = time.time() - start_oracle

    # Run Agent
    start_agent = time.time()
    try:
        subprocess.run([executable, data_file, agent_output], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent binary failed to run:\n{e.stderr}")
    agent_time = time.time() - start_agent

    assert os.path.isfile(oracle_output), "Oracle output file was not created"
    assert os.path.isfile(agent_output), "Agent output file was not created"

    # Calculate Speedup
    speedup = oracle_time / agent_time
    assert speedup >= 3.0, f"Speedup is {speedup:.2f}x, which is less than the required 3.0x threshold"

    # Calculate Accuracy
    try:
        oracle_df = pd.read_csv(oracle_output, names=["a", "b"])
    except Exception as e:
        pytest.fail(f"Failed to read oracle output CSV: {e}")

    try:
        agent_df = pd.read_csv(agent_output, names=["a", "b"])
    except Exception as e:
        pytest.fail(f"Failed to read agent output CSV: {e}")

    oracle_mean_a = oracle_df["a"].mean()
    oracle_mean_b = oracle_df["b"].mean()

    agent_mean_a = agent_df["a"].mean()
    agent_mean_b = agent_df["b"].mean()

    err_a = abs(oracle_mean_a - agent_mean_a)
    err_b = abs(oracle_mean_b - agent_mean_b)
    max_err = max(err_a, err_b)

    assert max_err <= 0.05, f"Maximum absolute error of parameter means is {max_err:.4f}, which exceeds the 0.05 threshold. Oracle means: a={oracle_mean_a:.4f}, b={oracle_mean_b:.4f}. Agent means: a={agent_mean_a:.4f}, b={agent_mean_b:.4f}."