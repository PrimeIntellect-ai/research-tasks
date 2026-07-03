# test_final_state.py

import os
import subprocess
import random

def test_relevance_fuzz_equivalence():
    agent_bin = "/home/user/relevance"
    oracle_bin = "/app/oracle_relevance"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"

    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary at {oracle_bin} is not executable"

    random.seed(42)
    # ASCII characters from 32 to 126
    chars = [chr(i) for i in range(32, 127)]

    for i in range(500):
        length = random.randint(0, 200)
        input_str = "".join(random.choice(chars) for _ in range(length))

        oracle_proc = subprocess.run(
            [oracle_bin, input_str],
            capture_output=True,
            text=True
        )
        oracle_out = oracle_proc.stdout.strip()

        agent_proc = subprocess.run(
            [agent_bin, input_str],
            capture_output=True,
            text=True
        )
        agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on iteration {i}.\n"
            f"Input: {repr(input_str)}\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output: {repr(agent_out)}"
        )