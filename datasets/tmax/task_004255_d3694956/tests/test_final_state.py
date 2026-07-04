# test_final_state.py

import os
import subprocess
import time
import pandas as pd
import pytest

def run_and_time(cmd):
    start = time.time()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    duration = time.time() - start
    assert result.returncode == 0, f"Command failed: {cmd}\nStdout: {result.stdout}\nStderr: {result.stderr}"
    return duration

def test_parallel_processor_speedup_and_correctness():
    go_script = "/home/user/parallel_processor.go"
    log_file = "/home/user/requests.log"
    oracle_bin = "/app/bucket_oracle"

    oracle_out = "/tmp/oracle_out.csv"
    agent_out = "/tmp/agent_out.csv"

    assert os.path.exists(go_script), f"Agent's Go program {go_script} does not exist."
    assert os.path.exists(log_file), f"Log file {log_file} does not exist."
    assert os.path.exists(oracle_bin), f"Legacy tool {oracle_bin} does not exist."

    # Remove previous outputs if they exist
    for f in [oracle_out, agent_out]:
        if os.path.exists(f):
            os.remove(f)

    # Run oracle
    t_oracle = run_and_time(f"{oracle_bin} {log_file} {oracle_out}")
    assert os.path.exists(oracle_out), f"Oracle output {oracle_out} was not created."

    # Run agent
    t_agent = run_and_time(f"go run {go_script} {log_file} {agent_out}")
    assert os.path.exists(agent_out), f"Agent output {agent_out} was not created."

    # Verify outputs match
    df_oracle = pd.read_csv(oracle_out)
    df_agent = pd.read_csv(agent_out)

    try:
        pd.testing.assert_frame_equal(df_oracle, df_agent, check_dtype=False, check_exact=True)
    except AssertionError as e:
        pytest.fail(f"Agent's output CSV does not match the oracle's output exactly.\nDetails: {e}")

    # Metric Threshold
    speedup = t_oracle / t_agent
    assert speedup >= 3.0, f"Speedup {speedup:.2f}x is below the 3.0x threshold (Oracle: {t_oracle:.2f}s, Agent: {t_agent:.2f}s)"