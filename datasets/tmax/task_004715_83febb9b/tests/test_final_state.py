# test_final_state.py

import os
import subprocess
import struct
import random
import tempfile
import pytest

ORACLE_PATH = "/opt/oracle/spectra_mean"
AGENT_PATH = "/home/user/spectra_mean"

def test_agent_program_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent program {AGENT_PATH} does not exist."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent program {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    random.seed(1337)
    num_tests = 20

    for i in range(num_tests):
        num_floats = random.randint(100, 10000)
        floats = [random.uniform(-10000.0, 10000.0) for _ in range(num_floats)]
        binary_data = struct.pack(f"<{num_floats}f", *floats)

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(binary_data)
            temp_path = f.name

        try:
            with open(temp_path, "rb") as f:
                oracle_proc = subprocess.run([ORACLE_PATH], stdin=f, capture_output=True, text=True)

            with open(temp_path, "rb") as f:
                agent_proc = subprocess.run([AGENT_PATH], stdin=f, capture_output=True, text=True)

            assert oracle_proc.returncode == 0, f"Oracle failed on input {i} with error: {oracle_proc.stderr}"
            assert agent_proc.returncode == 0, f"Agent failed on input {i} with error: {agent_proc.stderr}"

            assert oracle_proc.stdout == agent_proc.stdout, (
                f"Output mismatch on fuzz input {i} ({num_floats} floats).\n"
                f"Oracle output: {oracle_proc.stdout!r}\n"
                f"Agent output: {agent_proc.stdout!r}"
            )
        finally:
            os.remove(temp_path)