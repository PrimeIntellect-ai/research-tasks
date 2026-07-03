# test_final_state.py

import os
import json
import time
import subprocess
import pytest

def test_processor_go_exists():
    assert os.path.isfile("/home/user/processor.go"), "Missing file: /home/user/processor.go"

def test_output_and_speedup():
    agent_file = "/home/user/processor.go"
    output_file = "/home/user/output.json"
    oracle_bin = "/app/path_oracle"
    csv_file = "/home/user/transactions.csv"
    queries_file = "/home/user/queries.json"
    oracle_out = "/tmp/oracle_out.json"

    # Remove previous output if exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run Agent
    start_agent = time.time()
    try:
        subprocess.run(["go", "run", agent_file], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent program failed to execute:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}")
    agent_time = time.time() - start_agent

    assert os.path.isfile(output_file), f"Agent program did not produce {output_file}"
    with open(output_file) as f:
        try:
            agent_output = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {output_file} as valid JSON.")

    # Run Oracle
    start_oracle = time.time()
    try:
        subprocess.run([
            oracle_bin,
            f"--csv={csv_file}",
            f"--queries={queries_file}",
            f"--out={oracle_out}"
        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle program failed to execute:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}")
    oracle_time = time.time() - start_oracle

    assert os.path.isfile(oracle_out), f"Oracle program did not produce {oracle_out}"
    with open(oracle_out) as f:
        oracle_output = json.load(f)

    # Validate Accuracy
    assert agent_output == oracle_output, "Outputs do not match exactly! The Top 50 paths or their order differ from the oracle."

    # Validate Speedup
    speedup = oracle_time / agent_time
    assert speedup >= 4.0, f"Speedup {speedup:.2f} is below the 4.0x threshold. (Oracle: {oracle_time:.2f}s, Agent: {agent_time:.2f}s)"