# test_final_state.py

import os
import sys
import subprocess
import random
import io
import json
import pytest

def test_fastcsv_installed_and_fixed():
    # Check if fastcsv is installed and uses the C-extension
    try:
        import fastcsv
    except ImportError:
        pytest.fail("fastcsv is not installed in the environment.")

    # Check if it loads the C-extension
    try:
        import fastcsv._c_ext
    except ImportError:
        pytest.fail("fastcsv is installed but the C-extension (_c_ext) is not available. The build configuration was not fixed correctly.")

def generate_fuzz_input(seed, num_rows):
    rng = random.Random(seed)
    encodings = ['utf-8', 'iso-8859-1', 'cp1252']

    out = io.BytesIO()
    for _ in range(num_rows):
        row_id = rng.randint(1, 100000)
        encoding = rng.choice(encodings)

        # Generate random payload length
        payload_len = rng.randint(10, 100)
        # Generate random bytes, some might be invalid for the chosen encoding, which is fine (tests replacement)
        payload_bytes = bytearray(rng.getrandbits(8) for _ in range(payload_len))

        # Inject some newlines and commas
        for _ in range(rng.randint(0, 3)):
            idx = rng.randint(0, payload_len - 1)
            payload_bytes[idx] = ord(rng.choice([b'\n', b'\r', b',', b'"']))

        # To format as CSV, we need to escape quotes and wrap in quotes if necessary
        # Since it's raw bytes, we'll do a simple quote wrapping
        payload_escaped = payload_bytes.replace(b'"', b'""')
        payload_field = b'"' + payload_escaped + b'"'

        row = f"{row_id},{encoding},".encode('utf-8') + payload_field + b"\n"
        out.write(row)

    return out.getvalue()

def test_fuzz_equivalence():
    agent_script = "/home/user/stream_etl.py"
    oracle_bin = "/app/oracle/reference_etl_bin"

    assert os.path.isfile(agent_script), f"Agent script missing at {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Agent script at {agent_script} is not executable"

    # Fuzz testing
    N = 50 # Reduced from 500 to prevent test timeouts, but tests the same logic

    for i in range(N):
        num_rows = random.randint(10, 50)
        csv_data = generate_fuzz_input(seed=i, num_rows=num_rows)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin],
            input=csv_data,
            capture_output=True,
            timeout=5
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}:\n{oracle_proc.stderr.decode('utf-8', errors='replace')}"
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [sys.executable, agent_script],
            input=csv_data,
            capture_output=True,
            timeout=10
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed on iteration {i} with return code {agent_proc.returncode}.\nStderr: {agent_proc.stderr.decode('utf-8', errors='replace')}")

        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            # Try to decode to show a nice error
            try:
                oracle_str = oracle_out.decode('utf-8')
                agent_str = agent_out.decode('utf-8')
                error_msg = f"Mismatch on iteration {i}.\nOracle output:\n{oracle_str}\nAgent output:\n{agent_str}"
            except Exception:
                error_msg = f"Mismatch on iteration {i} (binary diff)."
            pytest.fail(error_msg)