# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/oracle_processor"
AGENT_SCRIPT = "/home/user/processor.py"
NUM_TESTS = 500
MAX_LENGTH = 2048

def generate_fuzz_input(length):
    # Biased towards pipes, spaces, and permutations of "error"
    special_chunks = [
        b'|', b' ', b'error', b'Error', b'ERROR', b'eRrOr', b'ErRoR',
        b'\x81', b'\x8d', b'\x8f', b'\x90', b'\x9d' # cp1252 undefined bytes
    ]
    all_bytes = [bytes([i]) for i in range(256)]

    out = bytearray()
    while len(out) < length:
        if random.random() < 0.4:
            out += random.choice(special_chunks)
        else:
            out += random.choice(all_bytes)
    return bytes(out[:length])

def test_agent_script_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle at {ORACLE_PATH} is not executable"

    random.seed(42)

    for i in range(NUM_TESTS):
        length = random.randint(0, MAX_LENGTH)
        test_input = generate_fuzz_input(length)

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=test_input,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {test_input!r}"
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            ["python3", AGENT_SCRIPT],
            input=test_input,
            capture_output=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed (exit code {agent_proc.returncode}) on input:\n{test_input!r}\nStderr:\n{agent_proc.stderr.decode(errors='replace')}")

        agent_output = agent_proc.stdout

        if oracle_output != agent_output:
            pytest.fail(
                f"Mismatch on fuzz iteration {i}.\n"
                f"Input (length {length}): {test_input!r}\n"
                f"Oracle output: {oracle_output!r}\n"
                f"Agent output:  {agent_output!r}"
            )