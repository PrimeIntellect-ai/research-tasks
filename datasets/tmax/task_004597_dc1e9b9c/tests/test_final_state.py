# test_final_state.py
import os
import subprocess
import random
import pytest

def test_query_engine_fuzz_equivalence():
    agent_bin = "/home/user/query_engine"
    oracle_bin = "/app/oracle/reference_engine"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary is not executable: {agent_bin}"

    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary is not executable: {oracle_bin}"

    random.seed(42)
    N = 1000

    for _ in range(N):
        source = random.randint(1, 200)
        target = random.randint(1, 200)

        # Run agent
        agent_res = subprocess.run([agent_bin, str(source), str(target)], capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent binary failed on input '{source} {target}'.\nStderr: {agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        # Run oracle
        oracle_res = subprocess.run([oracle_bin, str(source), str(target)], capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle binary failed on input '{source} {target}'.\nStderr: {oracle_res.stderr}"
        oracle_out = oracle_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on input '{source} {target}'.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )