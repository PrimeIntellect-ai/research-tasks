# test_final_state.py

import os
import random
import string
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/generate_links.py"
ORACLE_SCRIPT = "/app/oracle"
N_ITERATIONS = 100

def generate_random_input(seed):
    random.seed(seed)
    num_records = random.randint(1, 20)
    records = []

    for _ in range(num_records):
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
        ext = random.choice(['zip', 'tar.gz', 'bin', 'elf'])
        integrity = random.choice(['VALID', 'CORRUPT'])

        lines = [
            f"File: {filename}",
            f"Ext: {ext}",
            f"Integrity: {integrity}"
        ]

        # Add random spaces and shuffle
        shuffled_lines = []
        for line in lines:
            parts = line.split(':', 1)
            left = " " * random.randint(0, 3) + parts[0] + " " * random.randint(0, 3)
            right = " " * random.randint(0, 3) + parts[1].strip() + " " * random.randint(0, 3)
            shuffled_lines.append(f"{left}:{right}")

        random.shuffle(shuffled_lines)
        records.append("\n".join(shuffled_lines))

    return "\n===\n".join(records) + "\n"

def test_agent_script_exists_and_executable():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_SCRIPT), f"Oracle script {ORACLE_SCRIPT} missing."
    assert os.access(ORACLE_SCRIPT, os.X_OK), f"Oracle script {ORACLE_SCRIPT} is not executable."

    for i in range(N_ITERATIONS):
        test_input = generate_random_input(seed=42 + i)

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_SCRIPT],
            input=test_input,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input:\n{test_input}\nError:\n{oracle_proc.stderr}"
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_SCRIPT],
            input=test_input,
            text=True,
            capture_output=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed (exit code {agent_proc.returncode}) on input:\n{test_input}\nStderr:\n{agent_proc.stderr}")

        agent_output = agent_proc.stdout

        if agent_output != oracle_output:
            pytest.fail(
                f"Mismatch on iteration {i+1}.\n\n"
                f"Input:\n{test_input}\n"
                f"Expected (Oracle):\n{oracle_output}\n\n"
                f"Got (Agent):\n{agent_output}"
            )