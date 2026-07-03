# test_final_state.py
import os
import subprocess
import struct
import random
import pytest

ORACLE_PATH = "/app/oracle_graph_parser"
AGENT_CMD = ["python3", "/home/user/solution/runner.py"]

def generate_input(seed):
    random.seed(seed)
    # Occasionally generate invalid magic to test error handling
    if random.random() < 0.05:
        magic = b"BADD"
    else:
        magic = b"GRPH"

    V = random.randint(1, 500)
    E = random.randint(0, 2000)

    data = bytearray(magic)
    data += struct.pack("<II", V, E)
    for _ in range(E):
        u = random.randint(0, V - 1)
        v = random.randint(0, V - 1)
        data += struct.pack("<II", u, v)

    return bytes(data)

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"
    assert os.path.isfile(AGENT_CMD[1]), f"Agent runner script missing at {AGENT_CMD[1]}"

    for i in range(1000):
        data = generate_input(i)

        oracle_proc = subprocess.run([ORACLE_PATH], input=data, capture_output=True)
        agent_proc = subprocess.run(AGENT_CMD, input=data, capture_output=True)

        oracle_out = oracle_proc.stdout
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Output mismatch on iteration {i} (seed {i}).\n"
                f"Input length: {len(data)} bytes\n"
                f"Oracle output: {oracle_out!r}\n"
                f"Agent output: {agent_out!r}\n"
                f"Agent stderr: {agent_proc.stderr!r}"
            )