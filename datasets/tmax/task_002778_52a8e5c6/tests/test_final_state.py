# test_final_state.py

import os
import struct
import random
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/oracle_parser"
AGENT_SCRIPT = "/home/user/parse_wal.py"
N = 200

def generate_wal_file(path, seed):
    """Generate a random WAL file according to the specification."""
    rng = random.Random(seed)
    with open(path, "wb") as f:
        f.write(b"WALDATA1")
        num_records = rng.randint(0, 5000)
        for _ in range(num_records):
            length = rng.randint(0, 4096)
            rtype = rng.randint(0, 10)
            # Generate random payload bytes
            payload = bytearray(rng.getrandbits(8) for _ in range(length))
            f.write(struct.pack("<IB", length, rtype))
            f.write(payload)

def test_parse_wal_exists():
    """Verify that the agent script has been created."""
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

def test_fuzz_equivalence():
    """Fuzz both the oracle and the agent script to ensure bit-exact equivalence."""
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

    with tempfile.TemporaryDirectory() as tmpdir:
        wal_path = os.path.join(tmpdir, "test.wal")

        for i in range(N):
            generate_wal_file(wal_path, seed=1000 + i)

            oracle_cmd = [ORACLE_PATH, wal_path]
            agent_cmd = ["python3", AGENT_SCRIPT, wal_path]

            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

            assert oracle_res.returncode == 0, f"Oracle failed unexpectedly on iteration {i}."
            assert agent_res.returncode == 0, (
                f"Agent script failed on iteration {i}.\n"
                f"Stderr: {agent_res.stderr}"
            )

            oracle_out = oracle_res.stdout.strip()
            agent_out = agent_res.stdout.strip()

            assert oracle_out == agent_out, (
                f"Output mismatch on iteration {i} (seed {1000 + i}).\n"
                f"Expected (Oracle): {oracle_out}\n"
                f"Got (Agent):       {agent_out}\n"
            )