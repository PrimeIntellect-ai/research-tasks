# test_final_state.py

import os
import subprocess
import random
import pytest

def test_feature_extractor_exists():
    path = "/home/user/feature_extractor"
    assert os.path.isfile(path), f"Missing required compiled binary: {path}"
    assert os.access(path, os.X_OK), f"Compiled binary is not executable: {path}"

def test_fuzz_equivalence():
    agent_bin = "/home/user/feature_extractor"
    oracle_bin = "/app/oracle_feature_extractor"

    assert os.path.isfile(oracle_bin), f"Missing oracle binary: {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary not executable: {oracle_bin}"

    random.seed(42)
    N = 1000
    for i in range(N):
        # Generate 64 random floats
        input_floats = [random.uniform(-100.0, 100.0) for _ in range(64)]
        input_str = " ".join(f"{x:.6f}" for x in input_floats) + "\n"

        # Run oracle
        proc_oracle = subprocess.run(
            [oracle_bin],
            input=input_str,
            text=True,
            capture_output=True
        )
        assert proc_oracle.returncode == 0, f"Oracle failed on iteration {i}. Stderr: {proc_oracle.stderr}"
        oracle_out = proc_oracle.stdout.strip()

        # Run agent
        proc_agent = subprocess.run(
            [agent_bin],
            input=input_str,
            text=True,
            capture_output=True
        )
        assert proc_agent.returncode == 0, f"Agent binary failed on iteration {i}. Stderr: {proc_agent.stderr}"
        agent_out = proc_agent.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on iteration {i}.\n"
            f"Input (first 5 floats): {input_floats[:5]}...\n"
            f"Expected (Oracle): '{oracle_out}'\n"
            f"Got (Agent): '{agent_out}'"
        )