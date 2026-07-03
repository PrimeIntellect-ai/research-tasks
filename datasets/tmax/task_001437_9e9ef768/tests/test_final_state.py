# test_final_state.py

import os
import json
import random
import string
import subprocess
import pytest

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_input_data(n=1000, seed=42):
    random.seed(seed)
    lines = []
    for _ in range(n):
        if random.random() < 0.9:
            # Valid JSON
            obj = {
                "timestamp": random.randint(1600000000, 1700000000),
                "severity": random.randint(0, 100),
                "source": generate_random_string(random.randint(5, 15)),
                "message": generate_random_string(random.randint(10, 50))
            }
            lines.append(json.dumps(obj))
        else:
            # Malformed or missing keys
            if random.random() < 0.5:
                # Malformed JSON
                lines.append("{malformed json " + generate_random_string(10))
            else:
                # Missing keys
                obj = {
                    "timestamp": random.randint(1600000000, 1700000000),
                    "severity": random.randint(0, 100)
                }
                lines.append(json.dumps(obj))
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    agent_script = "/home/user/alert_parser.py"
    oracle_bin = "/app/oracle_parser"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.exists(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    input_data = generate_input_data(n=1000, seed=1337)

    # Run oracle
    oracle_proc = subprocess.run(
        [oracle_bin],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed with error: {oracle_proc.stderr}"
    oracle_output = oracle_proc.stdout

    # Run agent
    agent_proc = subprocess.run(
        ["python3", agent_script],
        input=input_data,
        text=True,
        capture_output=True
    )

    agent_output = agent_proc.stdout

    oracle_lines = oracle_output.splitlines()
    agent_lines = agent_output.splitlines()
    input_lines = input_data.splitlines()

    assert len(agent_lines) == len(oracle_lines), (
        f"Output line count mismatch. Oracle: {len(oracle_lines)}, Agent: {len(agent_lines)}. "
        f"Agent stderr: {agent_proc.stderr}"
    )

    for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
        assert o_line == a_line, (
            f"Mismatch at line {i+1}:\n"
            f"Input: {input_lines[i]}\n"
            f"Expected (Oracle): {o_line}\n"
            f"Got (Agent): {a_line}"
        )