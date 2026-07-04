# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/log_aggregator"
AGENT_PATH = "/home/user/solution.sh"
N_TESTS = 500

def generate_input(seed):
    random.seed(seed)
    num_lines = random.randint(10, 1000)
    lines = []
    for _ in range(num_lines):
        choice = random.random()
        if choice < 0.60:
            ts = "".join(random.choices(string.digits, k=10))
            lvl = "".join(random.choices(string.ascii_uppercase, k=random.randint(3, 8)))
            garbage1 = "".join(random.choices(string.ascii_letters, k=random.randint(0, 10)))
            garbage2 = "".join(random.choices(string.ascii_letters, k=random.randint(0, 10)))
            lines.append(f"{garbage1} ts={ts} {garbage2} lvl={lvl}")
        elif choice < 0.80:
            garbage1 = "".join(random.choices(string.ascii_letters, k=random.randint(0, 10)))
            garbage2 = "".join(random.choices(string.ascii_letters, k=random.randint(0, 10)))
            lines.append(f"{garbage1}TRACE{garbage2}")
        else:
            garbage = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 20)))
            lines.append(garbage)
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing: {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle not executable: {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent solution missing: {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent solution not executable: {AGENT_PATH}"

    for i in range(N_TESTS):
        input_data = generate_input(i)

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, text=True, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_data, text=True, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on test {i}\nError: {oracle_proc.stderr}"
        assert agent_proc.returncode == 0, f"Agent failed on test {i}\nError: {agent_proc.stderr}"

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Mismatch on test {i}.\n"
                f"--- Input ---\n{input_data[:500]}...\n"
                f"--- Oracle Output ---\n{oracle_proc.stdout[:500]}...\n"
                f"--- Agent Output ---\n{agent_proc.stdout[:500]}..."
            )