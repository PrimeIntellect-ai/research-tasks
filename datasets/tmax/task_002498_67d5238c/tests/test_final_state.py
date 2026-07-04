# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_build_queries"
AGENT_PATH = "/home/user/build_queries"

def generate_fuzz_input():
    num_lines = random.randint(5, 50)
    lines = []
    for _ in range(num_lines):
        res_id = random.randint(1, 999999)
        issn_len = random.randint(8, 15)
        issn = ''.join(random.choices(string.ascii_uppercase + string.digits, k=issn_len))
        lines.append(f"{res_id},{issn}")
    return "\n".join(lines) + "\n"

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent file at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle file at {ORACLE_PATH} is not executable"

    random.seed(42)
    N = 100

    for i in range(N):
        fuzz_input = generate_fuzz_input()

        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=fuzz_input,
                text=True,
                capture_output=True,
                check=True,
                timeout=2
            )
            oracle_output = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input:\n{fuzz_input}\nError:\n{e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input:\n{fuzz_input}")

        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=fuzz_input,
                text=True,
                capture_output=True,
                check=True,
                timeout=2
            )
            agent_output = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent failed on input:\n{fuzz_input}\nError:\n{e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input:\n{fuzz_input}")

        assert oracle_output == agent_output, (
            f"Output mismatch on test case {i+1}!\n"
            f"Input:\n{fuzz_input}\n"
            f"Expected Output (Oracle):\n{oracle_output}\n"
            f"Actual Output (Agent):\n{agent_output}"
        )