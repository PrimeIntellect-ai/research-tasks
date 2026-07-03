# test_final_state.py

import os
import random
import subprocess
import pytest

def test_executable_exists():
    agent_path = "/home/user/signal_decoder/signal_decoder"
    assert os.path.isfile(agent_path), f"Agent executable {agent_path} does not exist. Did you compile the code?"
    assert os.access(agent_path, os.X_OK), f"Agent executable {agent_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_decoder"
    agent_path = "/home/user/signal_decoder/signal_decoder"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} missing."
    assert os.path.isfile(agent_path), f"Agent {agent_path} missing."

    random.seed(42)
    hex_chars = "0123456789abcdef"

    N = 1000
    for i in range(N):
        length = random.randint(8, 512) * 2  # 16 to 1024, always even
        fuzz_input = "".join(random.choice(hex_chars) for _ in range(length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=fuzz_input.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=fuzz_input.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on input {fuzz_input[:32]}...\n"
            f"Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Output mismatch on input {fuzz_input[:32]}...\n"
            f"Oracle output: {oracle_proc.stdout}\n"
            f"Agent output: {agent_proc.stdout}"
        )