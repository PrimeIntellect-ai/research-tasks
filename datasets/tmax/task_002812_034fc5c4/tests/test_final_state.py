# test_final_state.py
import os
import random
import string
import subprocess
import pytest

def generate_random_csv(num_lines: int) -> str:
    lines = []
    for _ in range(num_lines):
        timestamp = random.randint(0, 9999999)
        config_id = "".join(random.choices(string.ascii_uppercase, k=3))
        revision = random.randint(1, 1000)
        value_len = random.randint(1, 32)
        value = "".join(random.choices(string.ascii_letters + string.digits, k=value_len))
        lines.append(f"{timestamp},{config_id},{revision},{value}")
    return "\n".join(lines) + ("\n" if lines else "")

def test_agent_executable_exists():
    agent_path = "/home/user/dedup_processor"
    assert os.path.exists(agent_path), f"Missing agent executable: {agent_path}"
    assert os.path.isfile(agent_path), f"Agent path is not a file: {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent file is not executable: {agent_path}"

def test_fuzz_equivalence():
    oracle_path = "/app/dedup_oracle"
    agent_path = "/home/user/dedup_processor"

    assert os.path.exists(oracle_path), f"Missing oracle executable: {oracle_path}"
    assert os.path.exists(agent_path), f"Missing agent executable: {agent_path}"

    N = 250
    random.seed(42)

    for i in range(N):
        num_lines = random.randint(0, 5000)
        csv_input = generate_random_csv(num_lines)

        oracle_proc = subprocess.run(
            [oracle_path],
            input=csv_input,
            text=True,
            capture_output=True
        )

        agent_proc = subprocess.run(
            [agent_path],
            input=csv_input,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on input {i} (lines: {num_lines}). "
            f"Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}\n"
            f"Agent stderr: {agent_proc.stderr}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Output mismatch on input {i} (lines: {num_lines}).\n"
            f"Oracle Output:\n{oracle_proc.stdout}\n"
            f"Agent Output:\n{agent_proc.stdout}\n"
        )