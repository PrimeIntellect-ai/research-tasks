# test_final_state.py

import os
import random
import string
import subprocess
from datetime import datetime, timedelta
import pytest

ORACLE_PATH = "/app/oracle_parser"
AGENT_PATH = "/home/user/pipeline/parser"

def generate_fuzz_inputs(n=2000, seed=42):
    random.seed(seed)
    inputs = []

    start_date = datetime(1970, 1, 1)
    end_date = datetime(2037, 12, 31)
    delta = end_date - start_date

    # 40% valid dates
    for _ in range(int(n * 0.4)):
        random_days = random.randrange(delta.days)
        random_seconds = random.randrange(24*60*60)
        dt = start_date + timedelta(days=random_days, seconds=random_seconds)
        inputs.append(dt.strftime("%Y-%m-%d %H:%M:%S"))

    # 20% poison strings
    for _ in range(int(n * 0.2)):
        prefix_len = random.randint(0, 15)
        suffix_len = random.randint(0, 15)
        prefix = ''.join(random.choices(string.ascii_letters + string.digits + " ", k=prefix_len))
        suffix = ''.join(random.choices(string.ascii_letters + string.digits + " ", k=suffix_len))
        inputs.append(f"{prefix}POISON_X9A2B4C1D{suffix}")

    # 40% random garbage
    for _ in range(int(n * 0.4)):
        length = random.randint(5, 50)
        garbage = ''.join(random.choices(string.printable.replace('\n', '').replace('\r', ''), k=length))
        inputs.append(garbage)

    random.shuffle(inputs)
    return "\n".join(inputs) + "\n"

def test_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable is missing at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle parser is missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle parser at {ORACLE_PATH} is not executable"

    input_data = generate_fuzz_inputs(n=2000)

    try:
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle parser timed out on fuzz inputs.")

    try:
        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Agent parser timed out on fuzz inputs.")

    oracle_lines = oracle_proc.stdout.splitlines()
    agent_lines = agent_proc.stdout.splitlines()
    input_lines = input_data.splitlines()

    assert len(agent_lines) == len(oracle_lines), (
        f"Output line count mismatch. Expected {len(oracle_lines)}, got {len(agent_lines)}."
    )

    for i, (oracle_line, agent_line, input_line) in enumerate(zip(oracle_lines, agent_lines, input_lines)):
        assert oracle_line == agent_line, (
            f"Output mismatch at line {i+1}.\n"
            f"Input: {repr(input_line)}\n"
            f"Expected: {repr(oracle_line)}\n"
            f"Got: {repr(agent_line)}"
        )