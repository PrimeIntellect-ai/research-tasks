# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_parser"
AGENT_PATH = "/home/user/parser"
N_ITERATIONS = 1000

def generate_random_input():
    num_records = random.randint(0, 50)
    lines = []
    for _ in range(num_records):
        lines.append(f"EventID: {random.randint(1, 1000000)}")

        fields = [
            f"Severity: {random.choice(['INFO', 'WARN', 'ERROR', 'FATAL'])}",
            f"Temperature: {random.uniform(0.0, 100.0):.2f}",
            f"Battery: {random.uniform(0.0, 100.0):.1f}%",
            f"Message: {''.join(random.choices(string.ascii_letters + string.digits + ' ', k=random.randint(5, 50)))}"
        ]
        random.shuffle(fields)
        lines.extend(fields)
        lines.append("---")

    # Occasionally omit the trailing separator for the last record
    if num_records > 0 and random.random() < 0.1:
        lines.pop()

    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable is not executable at {AGENT_PATH}"
    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"

    random.seed(42)

    for i in range(N_ITERATIONS):
        input_data = generate_random_input()

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, text=True, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_data, text=True, capture_output=True)

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Mismatch on fuzz iteration {i}.\n"
                f"--- Input ---\n{input_data}\n"
                f"--- Oracle Output ---\n{oracle_proc.stdout}\n"
                f"--- Agent Output ---\n{agent_proc.stdout}\n"
            )