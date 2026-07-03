# test_final_state.py

import os
import random
import string
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/ws_normalizer.sh"
ORACLE_BINARY = "/app/oracle_ws_normalizer"
NUM_TESTS = 500

def test_agent_script_exists_and_executable():
    assert os.path.isfile(AGENT_SCRIPT), f"Expected agent script not found at {AGENT_SCRIPT}"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script at {AGENT_SCRIPT} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_BINARY), f"Oracle binary not found at {ORACLE_BINARY}"
    assert os.access(ORACLE_BINARY, os.X_OK), f"Oracle binary at {ORACLE_BINARY} is not executable"

    random.seed(42)
    charset = string.ascii_letters + string.digits + " "

    for _ in range(NUM_TESTS):
        length = random.randint(5, 200)
        fuzz_input = "".join(random.choice(charset) for _ in range(length))

        oracle_proc = subprocess.run(
            [ORACLE_BINARY, fuzz_input],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {fuzz_input!r}"
        oracle_output = oracle_proc.stdout

        agent_proc = subprocess.run(
            [AGENT_SCRIPT, fuzz_input],
            capture_output=True,
            text=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed (return code {agent_proc.returncode}) on input: {fuzz_input!r}\nStderr: {agent_proc.stderr}"
        agent_output = agent_proc.stdout

        assert agent_output == oracle_output, (
            f"Output mismatch on input: {fuzz_input!r}\n"
            f"Expected (Oracle): {oracle_output!r}\n"
            f"Actual (Agent): {agent_output!r}"
        )