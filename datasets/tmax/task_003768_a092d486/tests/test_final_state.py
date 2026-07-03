# test_final_state.py

import os
import random
import subprocess
import string
import pytest

ORACLE_PATH = "/opt/oracle/archiver_oracle"
AGENT_PATH = "/home/user/archiver"
N_TESTS = 50

@pytest.mark.parametrize("i", range(N_TESTS))
def test_fuzz_equivalence(i):
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable at {AGENT_PATH} is not executable"

    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle executable at {ORACLE_PATH} is not executable"

    # Set seed based on test index for reproducibility
    random.seed(42 + i)

    # Generate random even length between 10 and 100000
    length = random.randint(5, 50000) * 2
    hex_chars = "0123456789ABCDEF"
    input_str = "".join(random.choice(hex_chars) for _ in range(length))
    input_bytes = input_str.encode('ascii')

    # Run oracle
    try:
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            check=True
        )
        oracle_out = oracle_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle failed on test {i} with stderr: {e.stderr.decode(errors='replace')}")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Oracle timed out on test {i}")

    # Run agent
    try:
        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            check=True
        )
        agent_out = agent_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent failed on test {i} with stderr: {e.stderr.decode(errors='replace')}")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Agent timed out on test {i}")

    # Compare
    if oracle_out != agent_out:
        # Show a snippet of the mismatch
        mismatch_len = min(len(oracle_out), len(agent_out))
        diff_idx = -1
        for idx in range(mismatch_len):
            if oracle_out[idx] != agent_out[idx]:
                diff_idx = idx
                break
        if diff_idx == -1:
            diff_idx = mismatch_len

        snippet_start = max(0, diff_idx - 16)
        snippet_end = min(max(len(oracle_out), len(agent_out)), diff_idx + 16)

        oracle_snippet = oracle_out[snippet_start:snippet_end].hex()
        agent_snippet = agent_out[snippet_start:snippet_end].hex()

        pytest.fail(
            f"Output mismatch on test {i} (input length {length}).\n"
            f"Oracle output length: {len(oracle_out)}, Agent output length: {len(agent_out)}\n"
            f"First difference at byte {diff_idx}.\n"
            f"Oracle snippet around diff: {oracle_snippet}\n"
            f"Agent snippet around diff:  {agent_snippet}"
        )