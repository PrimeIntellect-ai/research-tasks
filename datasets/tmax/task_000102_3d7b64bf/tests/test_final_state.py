# test_final_state.py
import os
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    agent_script = "/home/user/router.py"
    oracle_script = "/oracle/router_oracle.py"

    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script not found at {oracle_script}"

    random.seed(42)

    for _ in range(100):
        src = random.randint(0, 99)
        dst = random.randint(0, 99)
        time_sec = random.randint(0, 59)

        args = [str(src), str(dst), str(time_sec)]

        # Run agent
        agent_cmd = ["python3", agent_script] + args
        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, timeout=5)
            agent_out = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on inputs: {args}")

        # Run oracle
        oracle_cmd = ["python3", oracle_script] + args
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, check=True)
        oracle_out = oracle_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on inputs src={src}, dst={dst}, time_sec={time_sec}.\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output: '{agent_out}'\n"
            f"Agent stderr: '{agent_res.stderr.strip()}'"
        )