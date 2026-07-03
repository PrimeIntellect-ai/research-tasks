# test_final_state.py
import os
import subprocess
import random
import pytest

AGENT_SCRIPT = "/home/user/query_graph.py"
ORACLE_SCRIPT = "/tmp/oracle_query.py"

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.exists(ORACLE_SCRIPT), f"Oracle script not found at {ORACLE_SCRIPT}"

    random.seed(42)
    N = 50

    for i in range(N):
        start_id = random.randint(1, 200)
        max_depth = random.randint(0, 6)
        page_number = random.randint(1, 5)

        agent_cmd = ["python3", AGENT_SCRIPT, str(start_id), str(max_depth), str(page_number)]
        oracle_cmd = ["python3", ORACLE_SCRIPT, str(start_id), str(max_depth), str(page_number)]

        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)

        assert agent_proc.returncode == 0, f"Agent script failed with error on input {start_id} {max_depth} {page_number}:\n{agent_proc.stderr}"
        assert oracle_proc.returncode == 0, f"Oracle script failed on input {start_id} {max_depth} {page_number}:\n{oracle_proc.stderr}"

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on run {i+1}/{N} with inputs:\n"
            f"start_id={start_id}, max_depth={max_depth}, page_number={page_number}\n\n"
            f"Expected (Oracle):\n{oracle_out}\n\n"
            f"Got (Agent):\n{agent_out}"
        )