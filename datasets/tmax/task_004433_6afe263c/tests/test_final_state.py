# test_final_state.py

import os
import random
import string
import csv
import io
import subprocess
import pytest

def generate_fuzz_data(num_lines=5000):
    random.seed(42)
    charset = string.ascii_letters + string.digits + string.punctuation + " "

    output = io.StringIO()
    writer = csv.writer(output)

    for _ in range(num_lines):
        row = []
        for _ in range(3):
            length = random.randint(5, 50)
            val = "".join(random.choices(charset, k=length))
            row.append(val)
        writer.writerow(row)

    return output.getvalue()

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_parser"
    agent_path = "/home/user/parser"

    assert os.path.exists(oracle_path), f"Oracle parser not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle parser is not executable: {oracle_path}"

    assert os.path.exists(agent_path), f"Agent parser not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent parser is not executable: {agent_path}"

    fuzz_data = generate_fuzz_data(5000)

    oracle_result = subprocess.run(
        [oracle_path],
        input=fuzz_data,
        text=True,
        capture_output=True
    )
    assert oracle_result.returncode == 0, f"Oracle failed with error: {oracle_result.stderr}"

    agent_result = subprocess.run(
        [agent_path],
        input=fuzz_data,
        text=True,
        capture_output=True
    )
    assert agent_result.returncode == 0, f"Agent program failed with error: {agent_result.stderr}"

    oracle_lines = oracle_result.stdout.splitlines()
    agent_lines = agent_result.stdout.splitlines()

    assert len(agent_lines) == len(oracle_lines), f"Output line count mismatch: expected {len(oracle_lines)}, got {len(agent_lines)}"

    for i, (expected, actual) in enumerate(zip(oracle_lines, agent_lines)):
        if expected != actual:
            # Find the original input line corresponding to this output
            input_lines = fuzz_data.splitlines()
            input_line = input_lines[i] if i < len(input_lines) else "<unknown>"
            pytest.fail(
                f"Mismatch at line {i + 1}.\n"
                f"Input:    {input_line}\n"
                f"Expected: {expected}\n"
                f"Actual:   {actual}"
            )