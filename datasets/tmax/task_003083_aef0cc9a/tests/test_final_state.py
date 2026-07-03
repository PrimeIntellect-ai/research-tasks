# test_final_state.py
import os
import random
import struct
import subprocess
import pytest

ORACLE_PATH = "/app/astro_filter"
AGENT_PATH = "/home/user/astro_fast/target/release/astro_fast"
NUM_FUZZ_ROUNDS = 100

def test_agent_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Path {AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"File {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"

    # Fixed seed for reproducibility
    rng = random.Random(42)

    for i in range(NUM_FUZZ_ROUNDS):
        # Generate random length between 2 and 10000
        length = rng.randint(2, 10000)

        # Generate list of floats with large mean and small variance
        # Normal distribution with mean 10^9 and stddev 1.0
        floats = [rng.gauss(1e9, 1.0) for _ in range(length)]

        # Pack as little-endian f64
        input_data = struct.pack(f"<{length}d", *floats)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=input_data,
                capture_output=True,
                check=True,
                timeout=5
            )
            oracle_output = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on round {i+1} with error: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on round {i+1}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=input_data,
                capture_output=True,
                check=True,
                timeout=5
            )
            agent_output = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent failed on round {i+1} with error: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on round {i+1}")

        # Compare outputs
        if oracle_output != agent_output:
            # Unpack to show the difference
            try:
                oracle_mean, oracle_var = struct.unpack("<dd", oracle_output)
                agent_mean, agent_var = struct.unpack("<dd", agent_output)
                diff_msg = (
                    f"Mismatch on round {i+1} (input length {length}):\n"
                    f"Oracle output: mean={oracle_mean}, variance={oracle_var} (hex: {oracle_output.hex()})\n"
                    f"Agent output:  mean={agent_mean}, variance={agent_var} (hex: {agent_output.hex()})"
                )
            except Exception:
                diff_msg = (
                    f"Mismatch on round {i+1} (input length {length}):\n"
                    f"Oracle output hex: {oracle_output.hex()}\n"
                    f"Agent output hex:  {agent_output.hex()}"
                )
            pytest.fail(diff_msg)