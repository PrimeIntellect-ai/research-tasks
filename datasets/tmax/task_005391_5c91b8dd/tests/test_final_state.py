# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_embedder_fuzz_equivalence():
    agent_exec = "/home/user/embedder"
    oracle_exec = "/app/oracle_embedder"

    assert os.path.isfile(agent_exec), f"Agent executable not found at {agent_exec}"
    assert os.access(agent_exec, os.X_OK), f"Agent file at {agent_exec} is not executable"

    assert os.path.isfile(oracle_exec), f"Oracle executable not found at {oracle_exec}"
    assert os.access(oracle_exec, os.X_OK), f"Oracle file at {oracle_exec} is not executable"

    random.seed(42)

    # Generate random alphanumeric strings of length 1 to 200
    charset = string.ascii_letters + string.digits
    inputs = []

    # Ensure we include an empty string to test Rule 4
    inputs.append("")

    for _ in range(1000):
        length = random.randint(1, 200)
        s = ''.join(random.choice(charset) for _ in range(length))
        inputs.append(s)

    input_data = "\n".join(inputs) + "\n"

    # Run oracle
    oracle_proc = subprocess.run(
        [oracle_exec],
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )
    oracle_output = oracle_proc.stdout.splitlines()

    # Run agent
    agent_proc = subprocess.run(
        [agent_exec],
        input=input_data,
        text=True,
        capture_output=True
    )

    assert agent_proc.returncode == 0, f"Agent executable crashed or returned non-zero exit code. Stderr: {agent_proc.stderr}"

    agent_output = agent_proc.stdout.splitlines()

    assert len(agent_output) == len(oracle_output), (
        f"Output line count mismatch. Expected {len(oracle_output)} lines, got {len(agent_output)} lines."
    )

    for i, (inp, oracle_line, agent_line) in enumerate(zip(inputs, oracle_output, agent_output)):
        assert oracle_line == agent_line, (
            f"Mismatch on line {i + 1}.\n"
            f"Input: {repr(inp)}\n"
            f"Expected output: {oracle_line}\n"
            f"Agent output: {agent_line}"
        )