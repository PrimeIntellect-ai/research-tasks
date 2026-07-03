# test_final_state.py

import os
import random
import subprocess
import pytest

def test_bashrc_math_scale_fixed():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"File {bashrc_path} does not exist."

    with open(bashrc_path, "r") as f:
        content = f.read()

    assert "export MATH_SCALE=6" in content, "The .bashrc file does not contain the corrected 'export MATH_SCALE=6'."
    assert "export MATH_SCALE=0" not in content, "The .bashrc file still contains the misconfigured 'export MATH_SCALE=0'."

def test_peak_result_correct():
    result_path = "/home/user/peak_result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "42500.125600", f"Expected peak result to be '42500.125600', but got '{content}'."

def test_fixed_extractor_fuzz_equivalence():
    agent_script = "/home/user/fixed_extractor.sh"
    oracle_script = "/app/oracle_extractor.sh"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} does not exist."
    assert os.access(oracle_script, os.X_OK), f"Oracle script {oracle_script} is not executable."

    random.seed(42)

    for _ in range(100):
        arg1 = round(random.uniform(100.0, 50000.0), 6)
        arg2 = round(random.uniform(-10.0, 10.0), 6)

        str_arg1 = f"{arg1:.6f}"
        str_arg2 = f"{arg2:.6f}"

        agent_proc = subprocess.run(
            [agent_script, str_arg1, str_arg2],
            capture_output=True,
            text=True
        )
        oracle_proc = subprocess.run(
            [oracle_script, str_arg1, str_arg2],
            capture_output=True,
            text=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed with args {str_arg1} {str_arg2}:\n{agent_proc.stderr}"
        assert oracle_proc.returncode == 0, f"Oracle script failed with args {str_arg1} {str_arg2}:\n{oracle_proc.stderr}"

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Fuzzing mismatch for inputs {str_arg1} and {str_arg2}.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )