# test_final_state.py
import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/legacy_scorer"
AGENT_PATH = "/home/user/new_scorer/target/release/new_scorer"
NUM_ITERATIONS = 1000

@pytest.mark.timeout(60)
def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent binary missing at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

    random.seed(42)

    for i in range(NUM_ITERATIONS):
        x1 = random.uniform(-100.0, 100.0)
        x2 = random.uniform(-100.0, 100.0)
        x3 = random.uniform(-100.0, 100.0)
        x4 = random.uniform(-100.0, 100.0)

        input_str = f"{x1:.6f},{x2:.6f},{x3:.6f},{x4:.6f}\n"

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_str,
            text=True,
            capture_output=True
        )
        oracle_out = oracle_proc.stdout.strip()

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_str,
            text=True,
            capture_output=True
        )
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on iteration {i+1}.\n"
            f"Input: {input_str.strip()}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )