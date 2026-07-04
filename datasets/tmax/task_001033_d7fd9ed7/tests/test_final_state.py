# test_final_state.py

import os
import subprocess
import string
import random
import pytest

ORACLE_PATH = "/app/legacy_indexer"
AGENT_PATH = "/home/user/indexer"
NUM_TESTS = 1000

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle executable at {ORACLE_PATH} is not executable"

    random.seed(42)
    printable_chars = string.printable.replace('\r', '').replace('\n', '')

    for i in range(NUM_TESTS):
        length = random.randint(1, 200)
        input_str = ''.join(random.choice(printable_chars) for _ in range(length))
        input_bytes = (input_str + '\n').encode('utf-8')

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2
        )
        oracle_out = oracle_proc.stdout

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2
        )
        agent_out = agent_proc.stdout

        assert oracle_out == agent_out, (
            f"Mismatch on fuzz input #{i+1}.\n"
            f"Input: {repr(input_str)}\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output: {repr(agent_out)}"
        )