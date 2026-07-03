# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_fuzz_input():
    year = random.randint(1970, 2038)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    sec = random.randint(0, 59)

    cat = random.choice(["INFO", "WARN", "ERROR", "DEBUG", "TRACE"])

    msg_len = random.randint(10, 100)
    chars = string.ascii_letters + string.digits + " @_.-"
    msg = "".join(random.choices(chars, k=msg_len))

    # Format: YYYY.DD.MM/HH:MM:SS
    return f"{year:04d}.{day:02d}.{month:02d}/{hour:02d}:{minute:02d}:{sec:02d}|{cat}|{msg}"

def test_fuzz_equivalence():
    agent_script = "/home/user/run.sh"
    oracle_binary = "/app/legacy_parser"

    assert os.path.exists(agent_script), f"Agent script {agent_script} not found."
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable."
    assert os.path.exists(oracle_binary), f"Oracle binary {oracle_binary} not found."

    random.seed(42)
    num_tests = 1000
    inputs = [generate_fuzz_input() for _ in range(num_tests)]
    input_str = "\n".join(inputs) + "\n"

    oracle_proc = subprocess.run(
        [oracle_binary],
        input=input_str,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle binary failed with error: {oracle_proc.stderr}"
    oracle_lines = oracle_proc.stdout.strip().split("\n")

    agent_proc = subprocess.run(
        [agent_script],
        input=input_str,
        text=True,
        capture_output=True
    )
    assert agent_proc.returncode == 0, f"Agent script failed with error: {agent_proc.stderr}"
    agent_lines = agent_proc.stdout.strip().split("\n")

    assert len(oracle_lines) == num_tests, f"Oracle did not output {num_tests} lines. Got {len(oracle_lines)}."
    assert len(agent_lines) == num_tests, f"Agent did not output {num_tests} lines. Got {len(agent_lines)}."

    for i, (inp, oracle_out, agent_out) in enumerate(zip(inputs, oracle_lines, agent_lines)):
        assert oracle_out == agent_out, (
            f"Mismatch on input {i+1}/{num_tests}:\n"
            f"Input:  {inp}\n"
            f"Oracle: {oracle_out}\n"
            f"Agent:  {agent_out}"
        )