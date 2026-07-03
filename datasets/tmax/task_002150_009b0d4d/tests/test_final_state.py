# test_final_state.py

import os
import subprocess
import random
import string
import urllib.parse
import pytest

ORACLE_PATH = "/app/oracle_tracker"
AGENT_PATH = "/home/user/config_tracker"
NUM_FUZZ_TESTS = 1000

def generate_fuzz_input(seed):
    random.seed(seed)
    lines = []
    num_lines = random.randint(5, 100)

    target_keys = ['host', 'port', 'timeout', 'retries']

    for _ in range(num_lines):
        if random.random() < 0.6:
            key = random.choice(target_keys)
            key = "".join(random.choice([c.lower(), c.upper()]) for c in key)
        else:
            key = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 10)))

        space1 = " " * random.randint(0, 3) + "\t" * random.randint(0, 2)
        space2 = " " * random.randint(0, 3) + "\t" * random.randint(0, 2)
        space3 = " " * random.randint(0, 3) + "\t" * random.randint(0, 2)
        space4 = " " * random.randint(0, 3) + "\t" * random.randint(0, 2)

        if key.lower() == 'retries' and random.random() < 0.8:
            val_int = random.randint(-50, 50)
            val = str(val_int)
        else:
            raw_val = "".join(random.choices(string.ascii_letters + string.digits + " -_.:/", k=random.randint(1, 30)))
            val = urllib.parse.quote(raw_val)

        if random.random() < 0.3:
            val = urllib.parse.quote(val)

        line = f"{space1}{key}{space2}:{space3}{val}{space4}"
        lines.append(line)

    return "\n".join(lines).encode('utf-8')

def test_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle {ORACLE_PATH} is not executable"

    for i in range(NUM_FUZZ_TESTS):
        input_data = generate_fuzz_input(i)

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_data, capture_output=True)

        oracle_stdout = oracle_proc.stdout.decode('utf-8', errors='replace')
        agent_stdout = agent_proc.stdout.decode('utf-8', errors='replace')

        if oracle_stdout != agent_stdout:
            input_str = input_data.decode('utf-8', errors='replace')
            pytest.fail(
                f"Mismatch on fuzz iteration {i}.\n\n"
                f"INPUT:\n{input_str}\n\n"
                f"EXPECTED OUTPUT (Oracle):\n{oracle_stdout}\n\n"
                f"ACTUAL OUTPUT (Agent):\n{agent_stdout}\n"
            )