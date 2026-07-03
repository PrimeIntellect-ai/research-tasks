# test_final_state.py
import os
import random
import subprocess
import pytest

def test_graph_bin_exists_and_size():
    path = "/home/user/graph.bin"
    assert os.path.isfile(path), f"Agent's materialized graph file missing at {path}"
    size = os.path.getsize(path)
    assert size == 16384, f"Agent's graph file is not exactly 16384 bytes, got {size}"

def test_query_engine_exists_and_executable():
    path = "/home/user/query_engine"
    assert os.path.isfile(path), f"Agent's query engine missing at {path}"
    assert os.access(path, os.X_OK), f"Agent's query engine at {path} is not executable"

def test_fuzz_equivalence():
    # Generate 10,000 random integers uniformly from [-50, 200]
    random.seed(42)
    fuzz_inputs = [str(random.randint(-50, 200)) for _ in range(10000)]
    input_str = "\n".join(fuzz_inputs) + "\n"

    oracle_cmd = ["/app/oracle_query_engine", "/app/oracle_graph.bin"]
    agent_cmd = ["/home/user/query_engine", "/home/user/graph.bin"]

    # Run the oracle
    try:
        oracle_proc = subprocess.run(
            oracle_cmd, input=input_str, text=True, capture_output=True, check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle failed to execute: {e}\nStderr: {e.stderr}")

    oracle_out = oracle_proc.stdout

    # Run the agent
    agent_proc = subprocess.run(
        agent_cmd, input=input_str, text=True, capture_output=True
    )

    assert agent_proc.returncode == 0, (
        f"Agent's query engine failed with return code {agent_proc.returncode}.\n"
        f"Stderr: {agent_proc.stderr}"
    )

    agent_out = agent_proc.stdout

    # Compare outputs
    if oracle_out != agent_out:
        oracle_lines = oracle_out.splitlines()
        agent_lines = agent_out.splitlines()

        for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
            if o_line != a_line:
                pytest.fail(
                    f"Output mismatch on input '{fuzz_inputs[i]}':\n"
                    f"Expected (Oracle): {o_line}\n"
                    f"Got (Agent)      : {a_line}"
                )

        if len(oracle_lines) != len(agent_lines):
            pytest.fail(
                f"Output length mismatch: Expected {len(oracle_lines)} lines, "
                f"got {len(agent_lines)} lines."
            )