# test_final_state.py
import os
import random
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/query_range.sh"
ORACLE_SCRIPT = "/app/oracle_query.sh"

def test_agent_script_exists_and_executable():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle script {ORACLE_SCRIPT} does not exist."
    assert os.access(ORACLE_SCRIPT, os.X_OK), f"Oracle script {ORACLE_SCRIPT} is not executable."

    random.seed(42)

    for i in range(200):
        a = random.randint(1, 120)
        b = random.randint(1, 120)
        start_sec = min(a, b)
        end_sec = max(a, b)

        # Run oracle
        oracle_cmd = [ORACLE_SCRIPT, str(start_sec), str(end_sec)]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {start_sec} {end_sec}: {oracle_res.stderr}"
        oracle_out = oracle_res.stdout.strip()

        # Run agent
        agent_cmd = [AGENT_SCRIPT, str(start_sec), str(end_sec)]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        agent_out = agent_res.stdout.strip()

        if agent_res.returncode != 0:
            pytest.fail(f"Agent script failed on input '{start_sec} {end_sec}'.\nStderr: {agent_res.stderr}")

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on input: {start_sec} {end_sec}\n"
                f"Expected (Oracle): {oracle_out}\n"
                f"Got (Agent):       {agent_out}"
            )