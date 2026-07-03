# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/reference_encoder"
AGENT_PATH = "/home/user/monitor_fixed"
NUM_TESTS = 1000
TIMEOUT_SECONDS = 2.0

def test_agent_binary_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent binary {AGENT_PATH} does not exist."
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} does not exist."
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable."

    random.seed(42)
    charset = string.ascii_letters + string.digits + string.punctuation + " \t\n"

    for i in range(NUM_TESTS):
        length = random.randint(1, 1024)
        # Generate some runs to specifically test the RLE logic
        if random.random() < 0.3:
            # Generate a string with repeated characters
            char = random.choice(charset)
            input_data = (char * length).encode('utf-8')
        else:
            input_data = "".join(random.choice(charset) for _ in range(length)).encode('utf-8')

        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=input_data,
                capture_output=True,
                timeout=TIMEOUT_SECONDS,
                check=True
            )
            oracle_output = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle binary timed out on input of length {length}.")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle binary failed with return code {e.returncode}.")

        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=input_data,
                capture_output=True,
                timeout=TIMEOUT_SECONDS
            )
        except subprocess.TimeoutExpired:
            pytest.fail(
                f"Agent binary timed out (infinite loop?) on input of length {length}.\n"
                f"Input preview: {input_data[:100]!r}..."
            )

        assert agent_proc.returncode == 0, f"Agent binary failed with return code {agent_proc.returncode} on input of length {length}."

        assert agent_proc.stdout == oracle_output, (
            f"Output mismatch on input of length {length}.\n"
            f"Input preview: {input_data[:100]!r}...\n"
            f"Expected (Oracle): {oracle_output[:100]!r}...\n"
            f"Got (Agent): {agent_proc.stdout[:100]!r}..."
        )