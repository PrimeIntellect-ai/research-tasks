# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

ORACLE_PATH = "/app/oracle_bin"
AGENT_ENTRY = ["python3", "/home/user/repo/main.py"]
N_ITERATIONS = 50
MIN_LEN = 1024
MAX_LEN = 1048576

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.exists("/home/user/repo/main.py"), "Agent entry point missing"

    random.seed(42)

    for i in range(N_ITERATIONS):
        length = random.randint(MIN_LEN, MAX_LEN)
        # Generate random bytes
        input_bytes = random.randbytes(length)

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(input_bytes)
            tmp_path = tmp.name

        try:
            # Run oracle
            oracle_proc = subprocess.run(
                [ORACLE_PATH, tmp_path],
                capture_output=True,
                check=False
            )
            assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i} with error: {oracle_proc.stderr.decode(errors='replace')}"
            oracle_out = oracle_proc.stdout

            # Run agent
            agent_proc = subprocess.run(
                AGENT_ENTRY + [tmp_path],
                capture_output=True,
                check=False
            )
            assert agent_proc.returncode == 0, f"Agent failed on iteration {i} with error: {agent_proc.stderr.decode(errors='replace')}"
            agent_out = agent_proc.stdout

            assert agent_out == oracle_out, (
                f"Output mismatch on iteration {i} (input length {length}).\n"
                f"Oracle output len: {len(oracle_out)}\n"
                f"Agent output len: {len(agent_out)}"
            )
        finally:
            os.remove(tmp_path)