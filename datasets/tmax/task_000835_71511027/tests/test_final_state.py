# test_final_state.py

import os
import subprocess
import random
import pytest
from datetime import datetime, timedelta

AGENT_SCRIPT = "/home/user/process_line.py"
BASH_SCRIPT = "/home/user/run_pipeline.sh"
ORACLE_SCRIPT = "/app/oracle_processor.py"

def test_files_exist():
    """Verify that the required scripts were created."""
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script missing: {AGENT_SCRIPT}"
    assert os.path.isfile(BASH_SCRIPT), f"Bash script missing: {BASH_SCRIPT}"

def generate_valid_string():
    year = random.randint(2000, 2025)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 58)
    second = random.randint(0, 58)

    start_dt = datetime(year, month, day, hour, minute, second)
    end_dt = start_dt + timedelta(seconds=random.randint(0, 60))

    val = round(random.uniform(-1000.0, 1000.0), 2)
    status_len = random.randint(2, 8)
    status = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=status_len))

    start_str = start_dt.strftime('%Y-%m-%dT%H:%M:%S')
    end_str = end_dt.strftime('%Y-%m-%dT%H:%M:%S')

    return f"[{start_str}] TO [{end_str}] VALUE: {val} STATUS: {status}"

def generate_invalid_string():
    base = generate_valid_string()
    corruption_type = random.randint(0, 5)
    if corruption_type == 0:
        return base.replace("TO", "UNTIL")
    elif corruption_type == 1:
        return base.replace("[", "", 1)
    elif corruption_type == 2:
        return base + " EXTRA"
    elif corruption_type == 3:
        return base.replace("VALUE:", "VAL:")
    elif corruption_type == 4:
        return base.replace("STATUS:", "STAT:")
    else:
        return "completely invalid string with random data 12345"

def run_script(script_path, input_str):
    cmd = ["python3", script_path]
    result = subprocess.run(
        cmd,
        input=input_str.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode('utf-8').strip()

def test_fuzz_equivalence():
    """Fuzz test the agent script against the oracle script."""
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle missing: {ORACLE_SCRIPT}"

    random.seed(42)

    inputs = []
    for _ in range(250):
        inputs.append(generate_valid_string())
    for _ in range(250):
        inputs.append(generate_invalid_string())

    random.shuffle(inputs)

    for i, test_input in enumerate(inputs):
        oracle_output = run_script(ORACLE_SCRIPT, test_input)
        agent_output = run_script(AGENT_SCRIPT, test_input)

        assert oracle_output == agent_output, (
            f"Output mismatch on iteration {i}.\n"
            f"Input:\n{test_input}\n"
            f"Expected (Oracle):\n{oracle_output}\n"
            f"Got (Agent):\n{agent_output}"
        )