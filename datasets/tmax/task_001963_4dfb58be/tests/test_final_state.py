# test_final_state.py

import os
import subprocess
import random
import pytest

def test_graph_audit_script_exists():
    assert os.path.isfile('/home/user/graph_audit.py'), "/home/user/graph_audit.py does not exist."

def test_fuzz_equivalence():
    agent_script = '/home/user/graph_audit.py'
    oracle_script = '/app/oracle_audit.py'

    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} missing!"

    random.seed(42)
    # Fuzz-input distribution: N=100. Random integers between 1 and 1000 representing account_id.
    test_inputs = [random.randint(1, 1000) for _ in range(100)]

    for account_id in test_inputs:
        # Run oracle
        oracle_cmd = ['python3', oracle_script, str(account_id)]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {account_id}:\n{oracle_res.stderr}"
        oracle_out = oracle_res.stdout.strip()

        # Run agent
        agent_cmd = ['python3', agent_script, str(account_id)]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on input {account_id}:\n{agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on account_id={account_id}.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )