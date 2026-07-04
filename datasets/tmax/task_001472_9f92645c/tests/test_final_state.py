# test_final_state.py

import os
import random
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/dataset_recommender.sh"
ORACLE_SCRIPT = "/app/oracle_recommender.sh"

def test_agent_script_exists_and_executable():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable."

def generate_fuzz_input(lines_per_run=5):
    lines = []
    for _ in range(lines_per_run):
        ds_id = f"DS{random.randint(0, 999):03d}"
        threshold = f"{random.randint(0, 9)}.{random.randint(0, 99):02d}"
        lines.append(f"{ds_id} {threshold}")
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    random.seed(42)
    iterations = 20
    lines_per_run = 5

    for i in range(iterations):
        fuzz_input = generate_fuzz_input(lines_per_run)

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_SCRIPT],
            input=fuzz_input,
            text=True,
            capture_output=True
        )
        oracle_stdout = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_SCRIPT],
            input=fuzz_input,
            text=True,
            capture_output=True
        )
        agent_stdout = agent_proc.stdout

        # Compare
        if oracle_stdout != agent_stdout:
            error_msg = (
                f"Mismatch on iteration {i+1}.\n\n"
                f"Input:\n{fuzz_input}\n"
                f"Oracle Output:\n{oracle_stdout}\n"
                f"Agent Output:\n{agent_stdout}\n"
            )
            pytest.fail(error_msg)