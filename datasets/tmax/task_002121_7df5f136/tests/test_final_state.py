# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_fuzz_input(num_lines: int) -> str:
    lines = []
    for _ in range(num_lines):
        # 15% chance to be empty for X
        if random.random() < 0.15:
            x_str = ""
        else:
            x_str = f"{random.uniform(-100.0, 100.0):.2f}"

        # 15% chance to be empty for Y
        if random.random() < 0.15:
            y_str = ""
        else:
            y_str = f"{random.uniform(-100.0, 100.0):.2f}"

        lines.append(f"{x_str},{y_str}")
    return "\n".join(lines) + "\n"

def test_pipeline_exists_and_executable():
    agent_bin = "/home/user/pipeline"
    assert os.path.isfile(agent_bin), f"Agent binary {agent_bin} is missing."
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable."

def test_fuzz_equivalence():
    agent_bin = "/home/user/pipeline"
    oracle_bin = "/app/oracle_pipeline"

    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} is missing."
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable."

    random.seed(42)

    for i in range(100):
        num_lines = random.randint(50, 500)
        csv_input = generate_fuzz_input(num_lines)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin],
            input=csv_input,
            text=True,
            capture_output=True,
            check=False
        )

        # Run agent
        agent_proc = subprocess.run(
            [agent_bin],
            input=csv_input,
            text=True,
            capture_output=True,
            check=False
        )

        # Compare
        oracle_stdout = oracle_proc.stdout.strip()
        agent_stdout = agent_proc.stdout.strip()

        if oracle_stdout != agent_stdout:
            error_msg = (
                f"Mismatch on fuzz iteration {i}.\n"
                f"Input lines: {num_lines}\n"
                f"--- Oracle Output ---\n{oracle_stdout}\n"
                f"--- Agent Output ---\n{agent_stdout}\n"
                f"--- Input snippet ---\n{csv_input[:200]}...\n"
            )
            pytest.fail(error_msg)