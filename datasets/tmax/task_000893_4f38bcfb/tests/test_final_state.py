# test_final_state.py

import os
import subprocess
import random
import pytest

def test_generate_row_exists_and_executable():
    path = "/home/user/generate_row.sh"
    assert os.path.isfile(path), f"The script {path} is missing."
    assert os.access(path, os.X_OK), f"The script {path} is not executable."

def test_benchmark_script_exists_and_executable():
    path = "/home/user/benchmark.sh"
    assert os.path.isfile(path), f"The script {path} is missing."
    assert os.access(path, os.X_OK), f"The script {path} is not executable."

def test_benchmark_log_exists_and_valid():
    log_path = "/home/user/benchmark.log"
    assert os.path.isfile(log_path), f"The log file {log_path} is missing. Did you run the benchmark script?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content, f"The log file {log_path} is empty."

    try:
        val = float(content)
        assert val >= 0, f"Benchmark time must be non-negative, got {val}."
    except ValueError:
        pytest.fail(f"Content of {log_path} is not a valid float: {content}")

def test_fuzz_equivalence():
    oracle = "/app/oracle_generate_row.sh"
    agent = "/home/user/generate_row.sh"

    # Ensure oracle is present and executable
    assert os.path.isfile(oracle), f"Oracle script missing at {oracle}."
    assert os.access(oracle, os.X_OK), f"Oracle script at {oracle} is not executable."

    # We will test 10 random integers between 0 and 9
    random.seed(42)
    inputs = [random.randint(0, 9) for _ in range(10)]

    for t in inputs:
        oracle_res = subprocess.run([oracle, str(t)], capture_output=True, text=True)
        agent_res = subprocess.run([agent, str(t)], capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on input {t}: {oracle_res.stderr}"
        assert agent_res.returncode == 0, f"Agent script failed on input {t}: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on input T={t}.\n"
            f"Expected (Oracle): '{oracle_out}'\n"
            f"Got (Agent): '{agent_out}'"
        )