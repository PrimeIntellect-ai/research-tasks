# test_final_state.py

import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/oracle_processor"
AGENT_PATH = "/home/user/processor"

def generate_csv_stream(seed):
    random.seed(seed)
    lines = random.randint(10, 500)
    out = []
    for _ in range(lines):
        ts = random.randint(1000000, 2000000)
        name_len = random.randint(5, 20)
        name_chars = []
        for _ in range(name_len):
            choice = random.random()
            if choice < 0.5:
                name_chars.append(random.choice(string.ascii_letters))
            elif choice < 0.8:
                name_chars.append(random.choice(string.digits))
            else:
                name_chars.append(chr(random.randint(0x00A1, 0x01FF)))
        name = "".join(name_chars)

        if random.random() < 0.2:
            val = -1.0
        else:
            val = round(random.uniform(0.0, 1000.0), 2)

        out.append(f"{ts},{name},{val}")
    return "\n".join(out) + "\n"

def test_agent_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Path is not a file: {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent file is not executable: {AGENT_PATH}"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"

    num_inputs = 100
    for i in range(num_inputs):
        csv_input = generate_csv_stream(seed=42 + i)

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=csv_input.encode('utf-8'),
            capture_output=True,
            check=True
        )
        oracle_output = oracle_proc.stdout.decode('utf-8')

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=csv_input.encode('utf-8'),
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent program failed with return code {agent_proc.returncode} on input:\n{csv_input[:200]}..."

        agent_output = agent_proc.stdout.decode('utf-8')

        if agent_output != oracle_output:
            pytest.fail(
                f"Mismatch found on fuzz iteration {i}.\n"
                f"Input (first 200 chars):\n{csv_input[:200]}\n\n"
                f"Oracle Output (first 200 chars):\n{oracle_output[:200]}\n\n"
                f"Agent Output (first 200 chars):\n{agent_output[:200]}\n"
            )