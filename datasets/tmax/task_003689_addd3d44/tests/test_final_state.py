# test_final_state.py
import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_archiver"
AGENT_PATH = "/home/user/archiver/target/release/archiver"

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}. Did you run 'cargo build --release'?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable at {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle at {ORACLE_PATH} is not executable"

    random.seed(42)
    N = 100

    for i in range(N):
        length = random.randint(0, 8192)
        input_data = bytes(random.getrandbits(8) for _ in range(length))

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_data,
            capture_output=True,
            check=False
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input of length {length}"
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_data,
            capture_output=True,
            check=False
        )
        assert agent_proc.returncode == 0, f"Agent failed on input of length {length}. Stderr: {agent_proc.stderr.decode(errors='ignore')}"
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on random input of length {length}.\n"
                f"Expected {len(oracle_out)} bytes, got {len(agent_out)} bytes.\n"
                f"Oracle output (first 100 bytes): {oracle_out[:100]!r}\n"
                f"Agent output (first 100 bytes): {agent_out[:100]!r}"
            )