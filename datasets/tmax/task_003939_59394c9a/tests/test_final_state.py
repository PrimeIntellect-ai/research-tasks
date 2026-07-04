# test_final_state.py
import os
import random
import struct
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_filter"
AGENT_PATH = "/home/user/fixed_filter"
N_RUNS = 200

def generate_random_floats(n):
    return [random.uniform(-1000.0, 1000.0) for _ in range(n)]

def floats_to_bytes(floats):
    return struct.pack(f"<{len(floats)}f", *floats)

def run_program(executable, args, input_bytes):
    cmd = [executable] + [str(a) for a in args]
    result = subprocess.run(cmd, input=input_bytes, capture_output=True)
    return result.stdout, result.stderr, result.returncode

def test_fixed_filter_fuzz_equivalence():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable at {AGENT_PATH} is not executable"
    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"

    random.seed(42)

    for i in range(N_RUNS):
        num_floats = random.randint(1000, 10000)
        input_floats = generate_random_floats(num_floats)
        input_bytes = floats_to_bytes(input_floats)

        num_args = random.randint(1, 10)
        args = generate_random_floats(num_args)

        oracle_out, _, oracle_rc = run_program(ORACLE_PATH, args, input_bytes)
        agent_out, _, agent_rc = run_program(AGENT_PATH, args, input_bytes)

        assert agent_rc == oracle_rc, (
            f"Run {i}: Return code mismatch. Oracle: {oracle_rc}, Agent: {agent_rc}\n"
            f"Args: {args}"
        )
        assert agent_out == oracle_out, (
            f"Run {i}: Standard output mismatch.\n"
            f"Oracle output length: {len(oracle_out)} bytes\n"
            f"Agent output length: {len(agent_out)} bytes\n"
            f"Args: {args}"
        )