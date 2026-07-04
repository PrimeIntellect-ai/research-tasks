# test_final_state.py

import os
import struct
import subprocess
import tempfile
import random
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_bin"
    agent_path = "/home/user/compute_metric"

    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle binary is not executable at {oracle_path}"

    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary is not executable at {agent_path}"

    num_trials = 100
    num_doubles = 512

    # Use a fixed seed for reproducible fuzzing
    rng = random.Random(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_file_path = os.path.join(tmpdir, "input.bin")

        for trial in range(num_trials):
            # Generate 512 random doubles in [-10.0, 10.0]
            doubles = [rng.uniform(-10.0, 10.0) for _ in range(num_doubles)]

            # Pack into binary file (little-endian, IEEE 754 double precision)
            with open(input_file_path, "wb") as f:
                f.write(struct.pack(f"<{num_doubles}d", *doubles))

            # Run oracle
            oracle_result = subprocess.run(
                [oracle_path, input_file_path],
                capture_output=True,
                text=True,
                check=False
            )
            assert oracle_result.returncode == 0, f"Oracle failed on trial {trial} with stderr: {oracle_result.stderr}"
            oracle_output = oracle_result.stdout.strip()

            # Run agent
            agent_result = subprocess.run(
                [agent_path, input_file_path],
                capture_output=True,
                text=True,
                check=False
            )
            assert agent_result.returncode == 0, f"Agent binary failed on trial {trial} with stderr: {agent_result.stderr}"
            agent_output = agent_result.stdout.strip()

            # Compare outputs
            assert agent_output == oracle_output, (
                f"Mismatch on trial {trial}.\n"
                f"Oracle output: {oracle_output}\n"
                f"Agent output:  {agent_output}\n"
                f"Input data snippet: {doubles[:5]}..."
            )