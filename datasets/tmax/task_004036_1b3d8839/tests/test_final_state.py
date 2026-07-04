# test_final_state.py

import os
import subprocess
import random
import pytest

def test_max_anomaly_frame_file():
    path = "/home/user/max_anomaly_frame.txt"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "87", f"Expected max anomaly frame to be 87, but got {content}."

def test_scorer_binary_exists():
    path = "/home/user/vision_pipeline/bin/scorer"
    assert os.path.isfile(path), f"Agent binary {path} does not exist."
    assert os.access(path, os.X_OK), f"Agent binary {path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_scorer"
    agent_path = "/home/user/vision_pipeline/bin/scorer"

    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} does not exist."
    assert os.path.isfile(agent_path), f"Agent binary {agent_path} does not exist."

    random.seed(42)
    N = 1000  # Reduced from 10000 to avoid test timeout in standard CI, but still robust

    for i in range(N):
        # Generate exactly 4096 bytes of random data
        test_input = bytes(random.getrandbits(8) for _ in range(4096))

        oracle_proc = subprocess.run(
            [oracle_path],
            input=test_input,
            capture_output=True,
            timeout=2
        )
        agent_proc = subprocess.run(
            [agent_path],
            input=test_input,
            capture_output=True,
            timeout=2
        )

        assert oracle_proc.returncode == agent_proc.returncode, \
            f"Return code mismatch on iteration {i}. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, \
            f"Output mismatch on iteration {i}.\nOracle output: {oracle_out}\nAgent output: {agent_out}"