# test_final_state.py

import os
import subprocess
import random
import pytest
import math

def test_final_variance_file():
    variance_file = "/home/user/final_variance.txt"
    assert os.path.isfile(variance_file), f"Expected output file {variance_file} does not exist."

    with open(variance_file, "r") as f:
        content = f.read().strip()

    assert content, f"File {variance_file} is empty."
    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {variance_file} is not a valid float: {content}")

    # The truth mentions 482.105392, let's check if it's reasonably close
    assert math.isclose(val, 482.105392, rel_tol=1e-2), f"Final variance {val} is not close to expected 482.105392."

def test_stability_calc_executable():
    agent_bin = "/home/user/stability_calc"
    assert os.path.isfile(agent_bin), f"Agent binary {agent_bin} does not exist."
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable."

def test_fuzz_equivalence():
    agent_bin = "/home/user/stability_calc"
    oracle_bin = "/app/oracle_stability_calc"

    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} missing."
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable."

    random.seed(42)
    num_tests = 50

    for i in range(num_tests):
        seq_len = random.randint(10, 1000)
        input_floats = [random.uniform(0.0, 255.0) for _ in range(seq_len)]
        input_str = "\n".join(f"{x:.6f}" for x in input_floats) + "\n"

        # Run oracle
        proc_oracle = subprocess.run(
            [oracle_bin],
            input=input_str,
            text=True,
            capture_output=True
        )
        assert proc_oracle.returncode == 0, f"Oracle failed on input {i}"
        oracle_out = proc_oracle.stdout.strip()

        # Run agent
        proc_agent = subprocess.run(
            [agent_bin],
            input=input_str,
            text=True,
            capture_output=True
        )
        assert proc_agent.returncode == 0, f"Agent binary failed on input {i}\nError: {proc_agent.stderr}"
        agent_out = proc_agent.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on fuzz test {i} (length {seq_len}).\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output:  {agent_out}\n"
            f"Input preview: {input_str[:100]}..."
        )