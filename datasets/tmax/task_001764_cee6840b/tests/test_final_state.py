# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/relax_bin"
AGENT_PATH = "/home/user/relax_out"
NUM_TESTS = 100

def generate_input(seed):
    random.seed(seed)
    n = random.randint(10, 200)
    vals = [str(random.randint(-100, 100)) for _ in range(n)]
    return f">SEQ\n{' '.join(vals)}\n"

def run_program(executable, input_data):
    try:
        result = subprocess.run(
            [executable],
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
            timeout=5
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: Return code {e.returncode}\nStderr: {e.stderr}"
    except subprocess.TimeoutExpired:
        return "ERROR: Timeout"

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent file at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle file at {ORACLE_PATH} is not executable"

    for i in range(NUM_TESTS):
        input_data = generate_input(seed=42 + i)

        oracle_output = run_program(ORACLE_PATH, input_data)
        agent_output = run_program(AGENT_PATH, input_data)

        assert oracle_output == agent_output, (
            f"Mismatch on test case {i+1}/{NUM_TESTS}.\n"
            f"Input:\n{input_data}\n"
            f"Oracle output:\n{oracle_output}\n"
            f"Agent output:\n{agent_output}\n"
        )