# test_final_state.py

import os
import subprocess
import random
import pytest

def test_analyze_script_exists_and_executable():
    path = '/home/user/analyze.sh'
    assert os.path.isfile(path), f"Agent script {path} is missing."
    assert os.access(path, os.X_OK), f"Agent script {path} is not marked as executable."

def test_mcmc_estimate_compiled():
    path = '/app/stats-tools/mcmc_estimate'
    assert os.path.isfile(path), f"Compiled binary {path} is missing."
    assert os.access(path, os.X_OK), f"Compiled binary {path} is not executable."

def test_fuzz_equivalence():
    oracle_path = '/opt/oracle/analyze_oracle.sh'
    agent_path = '/home/user/analyze.sh'

    assert os.path.isfile(oracle_path), f"Oracle script {oracle_path} is missing."

    random.seed(42)
    N = 500

    for _ in range(N):
        o1 = random.randint(0, 50)
        o2 = random.randint(0, 50)
        e1 = random.randint(0, 50)
        e2 = random.randint(0, 50)

        args = [str(o1), str(o2), str(e1), str(e2)]

        oracle_res = subprocess.run([oracle_path] + args, capture_output=True, text=True)
        agent_res = subprocess.run([agent_path] + args, capture_output=True, text=True)

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on inputs (O1, O2, E1, E2) = {args}.\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output:  '{agent_out}'\n"
            f"Agent stderr:  '{agent_res.stderr.strip()}'"
        )