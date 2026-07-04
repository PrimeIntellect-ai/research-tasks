# test_final_state.py
import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/legacy_profiler.bin"
AGENT_SCRIPT = "/home/user/profiler_calc.py"
N_TESTS = 200

def generate_input():
    length = random.randint(5, 100)
    seq = [str(random.randint(10, 15000)) for _ in range(length)]
    return ",".join(seq)

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.path.exists(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} does not exist."

    random.seed(42)

    for i in range(N_TESTS):
        test_input = generate_input()

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH, test_input],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {test_input}\nStderr: {oracle_proc.stderr}"
        oracle_output = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["python3", AGENT_SCRIPT, test_input],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input: {test_input}\nStderr: {agent_proc.stderr}"
        agent_output = agent_proc.stdout.strip()

        assert agent_output == oracle_output, (
            f"Output mismatch on test {i+1}/{N_TESTS}.\n"
            f"Input: {test_input}\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )