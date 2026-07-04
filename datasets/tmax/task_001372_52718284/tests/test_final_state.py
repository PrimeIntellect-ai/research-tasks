# test_final_state.py

import os
import random
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/api_v3.py"
ORACLE_BIN = "/app/oracle_bin"

def test_api_v3_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} is missing."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_BIN), f"Oracle binary {ORACLE_BIN} is missing."

    random.seed(42)
    inputs = [random.randint(0, 300) for _ in range(20)]

    for frame_num in inputs:
        input_str = str(frame_num)

        # Run oracle
        oracle_cmd = [ORACLE_BIN, input_str]
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on input {input_str}:\n{oracle_proc.stderr}"
        oracle_output = oracle_proc.stdout.strip()

        # Run agent
        agent_cmd = ["python3", AGENT_SCRIPT, input_str]
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent script failed on input {input_str}:\n{agent_proc.stderr}"
        agent_output = agent_proc.stdout.strip()

        assert agent_output == oracle_output, (
            f"Mismatch on frame {input_str}.\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output: {agent_output}"
        )