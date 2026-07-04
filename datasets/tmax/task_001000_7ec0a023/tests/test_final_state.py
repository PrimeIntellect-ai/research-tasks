# test_final_state.py

import os
import random
import string
import subprocess
import pytest

AGENT_BIN = "/home/user/query_builder"
ORACLE_BIN = "/opt/oracle_query_builder"

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_BIN), f"Agent executable missing at {AGENT_BIN}"
    assert os.access(AGENT_BIN, os.X_OK), f"Agent executable is not executable: {AGENT_BIN}"

def generate_random_csv_input():
    num_lines = random.randint(1, 100)
    lines = []
    for _ in range(num_lines):
        tx_id = f"TX{random.randint(1000, 9999)}"
        from_acc = f"ACCT{random.choice(string.ascii_uppercase)}"

        # 10% chance to make from_acc and to_acc identical
        if random.random() < 0.1:
            to_acc = from_acc
        else:
            to_acc = f"ACCT{random.choice(string.ascii_uppercase)}"

        amount = random.randint(1, 10000)
        lines.append(f"{tx_id},{from_acc},{to_acc},{amount}")

    return "\n".join(lines) + "\n"

def run_program(executable, input_data):
    try:
        result = subprocess.run(
            [executable],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=5
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {executable} timed out.")
    except Exception as e:
        pytest.fail(f"Execution of {executable} failed: {e}")

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_BIN), f"Oracle executable missing at {ORACLE_BIN}"

    random.seed(42)

    for i in range(100):
        csv_input = generate_random_csv_input()

        oracle_stdout, oracle_stderr, oracle_rc = run_program(ORACLE_BIN, csv_input)
        agent_stdout, agent_stderr, agent_rc = run_program(AGENT_BIN, csv_input)

        if agent_stdout != oracle_stdout:
            error_msg = (
                f"Mismatch on iteration {i+1}.\n"
                f"Input:\n{csv_input}\n"
                f"Expected Output (Oracle):\n{oracle_stdout}\n"
                f"Actual Output (Agent):\n{agent_stdout}\n"
            )
            pytest.fail(error_msg)