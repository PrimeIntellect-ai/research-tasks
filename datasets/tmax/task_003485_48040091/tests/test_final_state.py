# test_final_state.py
import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/oracle"
AGENT_PATH = "/home/user/etl_transform"
N_TESTS = 50
LENGTH_RANGE = (100, 1000)
CHAR_SET = ["-2", "-1", "0", "1"]

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable at {AGENT_PATH} is not executable"

def generate_fuzz_input(seed):
    random.seed(seed)
    length = random.randint(*LENGTH_RANGE)
    return "\n".join(random.choices(CHAR_SET, k=length)) + "\n"

@pytest.mark.parametrize("seed", range(N_TESTS))
def test_fuzz_equivalence(seed):
    assert os.path.isfile(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent not found at {AGENT_PATH}"

    input_data = generate_fuzz_input(seed)

    # Run oracle
    oracle_proc = subprocess.run(
        [ORACLE_PATH],
        input=input_data,
        text=True,
        capture_output=True,
        check=False
    )

    # Run agent
    agent_proc = subprocess.run(
        [AGENT_PATH],
        input=input_data,
        text=True,
        capture_output=True,
        check=False
    )

    assert agent_proc.returncode == oracle_proc.returncode, (
        f"Return code mismatch on seed {seed}.\n"
        f"Oracle return code: {oracle_proc.returncode}\n"
        f"Agent return code: {agent_proc.returncode}"
    )

    assert agent_proc.stdout == oracle_proc.stdout, (
        f"Output mismatch on seed {seed}.\n"
        f"Input stream (first 100 chars): {input_data[:100]}...\n"
        f"Oracle output (first 200 chars): {oracle_proc.stdout[:200]}...\n"
        f"Agent output (first 200 chars): {agent_proc.stdout[:200]}..."
    )