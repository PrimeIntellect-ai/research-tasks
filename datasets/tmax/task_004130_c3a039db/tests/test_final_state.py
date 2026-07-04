# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_bin"
AGENT_PATH = "/home/user/fixed_aggregator"
N_TESTS = 500

def generate_fuzz_input():
    services = ["AUTH", "DB", "FRONTEND"]
    num_lines = random.randint(5, 50)
    lines = []
    for _ in range(num_lines):
        service = random.choice(services)
        timestamp = random.randint(1600000000, 1700000000)
        msg_len = random.randint(10, 50)
        msg = ''.join(random.choices(string.ascii_letters + string.digits, k=msg_len))
        lines.append(f"{service}|{timestamp}|{msg}")
    return "\n".join(lines) + "\n"

def test_fixed_aggregator_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Missing fixed binary at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Fixed binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary not executable"

    random.seed(42)

    for i in range(N_TESTS):
        fuzz_input = generate_fuzz_input()

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=fuzz_input,
            text=True,
            capture_output=True
        )

        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=fuzz_input,
                text=True,
                capture_output=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out (possible deadlock) on input {i}.\nInput:\n{fuzz_input}")

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on input {i}.\n"
            f"Oracle: {oracle_proc.returncode}\n"
            f"Agent: {agent_proc.returncode}\n"
            f"Input:\n{fuzz_input}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on input {i}.\n"
            f"Input:\n{fuzz_input}\n"
            f"Oracle output:\n{oracle_proc.stdout}\n"
            f"Agent output:\n{agent_proc.stdout}"
        )