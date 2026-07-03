# test_final_state.py
import os
import subprocess
import random
import pytest

def test_executable_exists():
    agent_bin = "/home/user/processor/target/release/processor"
    assert os.path.isfile(agent_bin), f"Agent executable not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent executable at {agent_bin} is not executable"

def test_fuzz_equivalence():
    oracle_bin = "/app/oracle"
    agent_bin = "/home/user/processor/target/release/processor"

    assert os.path.isfile(oracle_bin), f"Oracle executable not found at {oracle_bin}"
    assert os.path.isfile(agent_bin), f"Agent executable not found at {agent_bin}"

    random.seed(42)
    num_lines = 50
    input_lines = []
    for _ in range(num_lines):
        floats = [random.uniform(-10.0, 10.0) for _ in range(8)]
        line = " ".join(f"{f:.6f}" for f in floats)
        input_lines.append(line)

    input_text = "\n".join(input_lines) + "\n"

    # Run oracle
    try:
        oracle_proc = subprocess.run(
            [oracle_bin],
            input=input_text,
            text=True,
            capture_output=True,
            check=True,
            timeout=5
        )
        oracle_output = oracle_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle failed to run: {e.stderr}")

    # Run agent
    try:
        agent_proc = subprocess.run(
            [agent_bin],
            input=input_text,
            text=True,
            capture_output=True,
            check=True,
            timeout=5
        )
        agent_output = agent_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent program failed to run: {e.stderr}")

    oracle_lines = oracle_output.strip().split("\n")
    agent_lines = agent_output.strip().split("\n")

    assert len(agent_lines) == len(oracle_lines), f"Output line count mismatch. Expected {len(oracle_lines)}, got {len(agent_lines)}"

    for i, (oracle_line, agent_line) in enumerate(zip(oracle_lines, agent_lines)):
        assert agent_line.strip() == oracle_line.strip(), (
            f"Mismatch at line {i+1}.\n"
            f"Input: {input_lines[i]}\n"
            f"Expected (oracle): {oracle_line.strip()}\n"
            f"Got (agent):       {agent_line.strip()}"
        )