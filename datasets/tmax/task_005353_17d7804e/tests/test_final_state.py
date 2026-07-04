# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_parallel_fixed():
    parallel_script = "/app/parallel-20231022/src/parallel"
    assert os.path.isfile(parallel_script), f"GNU parallel script is missing at {parallel_script}"

    with open(parallel_script, 'r', encoding='utf-8', errors='ignore') as f:
        first_line = f.readline().strip()

    assert "pperl" not in first_line, f"The shebang in {parallel_script} still contains 'pperl'."
    assert "perl" in first_line, f"The shebang in {parallel_script} should contain 'perl'."

    # Check if parallel runs
    result = subprocess.run([parallel_script, "--version"], capture_output=True, text=True)
    assert result.returncode == 0, f"GNU parallel failed to run. Stderr: {result.stderr}"

def generate_random_csv(num_lines):
    lines = []
    for _ in range(num_lines):
        timestamp = random.randint(1600000000, 1700000000)
        sensor_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        value = random.randint(0, 1000)
        lines.append(f"{timestamp},{sensor_id},{value}")
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/reference_etl.sh"
    agent_path = "/home/user/etl.sh"

    assert os.path.isfile(agent_path), f"Agent script is missing at {agent_path}"
    assert os.access(agent_path, os.X_OK) or os.access(agent_path, os.R_OK), f"Agent script {agent_path} is not readable/executable."

    random.seed(42)
    N = 100

    for i in range(N):
        num_lines = random.randint(100, 10000)
        csv_input = generate_random_csv(num_lines)

        # Run oracle
        oracle_proc = subprocess.run(
            ["bash", oracle_path],
            input=csv_input,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}. Stderr: {oracle_proc.stderr}"
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            ["bash", agent_path],
            input=csv_input,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on iteration {i}. Stderr: {agent_proc.stderr}"
        agent_output = agent_proc.stdout

        assert agent_output == oracle_output, (
            f"Output mismatch on iteration {i} (input lines: {num_lines}).\n"
            f"--- Oracle Output ---\n{oracle_output}\n"
            f"--- Agent Output ---\n{agent_output}\n"
        )