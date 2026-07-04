# test_final_state.py

import os
import subprocess
import random
import pytest

def test_ci_build_script_exists():
    script_path = "/home/user/signal_project/ci_build.sh"
    assert os.path.isfile(script_path), f"CI/CD script {script_path} is missing."

def test_agent_binary_exists():
    agent_bin = "/home/user/signal_project/poly_tool_x86_64"
    assert os.path.isfile(agent_bin), f"Agent binary {agent_bin} is missing."
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable."

def test_fuzz_equivalence():
    oracle_bin = "/app/oracle_bin"
    agent_bin = "/home/user/signal_project/poly_tool_x86_64"

    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} is missing."
    assert os.path.isfile(agent_bin), f"Agent binary {agent_bin} is missing."

    random.seed(42)
    inputs = [random.randint(0, 50000) for _ in range(1000)]

    for val in inputs:
        val_str = str(val)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin, val_str],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle binary failed on input {val_str}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            [agent_bin, val_str],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent binary failed on input {val_str}"
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Output mismatch on input {val_str}.\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )