# test_final_state.py

import os
import subprocess
import random
import pytest

def test_fixed_pipeline_exists_and_executable():
    path = "/home/user/fixed_pipeline.sh"
    assert os.path.isfile(path), f"Expected fixed pipeline script at {path} does not exist."
    assert os.access(path, os.X_OK), f"Fixed pipeline script at {path} is not executable."

def test_helper_compiles_and_works():
    # The user was supposed to fix the Makefile and compile the helper.
    # We check if the helper binary exists and works.
    helper_path = "/home/user/src/helper"
    assert os.path.isfile(helper_path), f"Expected compiled helper binary at {helper_path} does not exist. Did you run make?"
    assert os.access(helper_path, os.X_OK), f"Helper binary at {helper_path} is not executable."

    # Test helper with a simple input
    result = subprocess.run([helper_path, "5"], capture_output=True, text=True)
    assert result.returncode == 0, f"Helper failed to run: {result.stderr}"
    assert result.stdout.strip() == "25", f"Helper produced incorrect output for input '5': {result.stdout.strip()}"

def test_fuzz_equivalence():
    agent_script = "/home/user/fixed_pipeline.sh"
    oracle_bin = "/app/oracle_calc"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} not found."
    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} not found."

    random.seed(42)
    inputs = [random.randint(-500, 500) for _ in range(100)]

    for x in inputs:
        x_str = str(x)

        # Run oracle
        oracle_res = subprocess.run([oracle_bin, x_str], capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {x_str}: {oracle_res.stderr}"
        oracle_out = oracle_res.stdout.strip()

        # Run agent script
        agent_res = subprocess.run(["/bin/bash", agent_script, x_str], capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on input {x_str}: {agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on input {x_str}.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent):       {agent_out}"
        )