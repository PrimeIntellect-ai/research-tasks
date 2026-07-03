# test_final_state.py

import os
import subprocess
import random
import struct
import pytest

def test_source_file_exists():
    """Verify that the student wrote the C++ source file."""
    source_path = "/home/user/ema_filter.cpp"
    assert os.path.exists(source_path), f"Source file missing: {source_path}"
    assert os.path.isfile(source_path), f"Path is not a file: {source_path}"

def test_executable_exists():
    """Verify that the student compiled the executable."""
    exec_path = "/home/user/ema_filter"
    assert os.path.exists(exec_path), f"Executable missing: {exec_path}"
    assert os.path.isfile(exec_path), f"Path is not a file: {exec_path}"
    assert os.access(exec_path, os.X_OK), f"File is not executable: {exec_path}"

def test_fuzz_equivalence():
    """Fuzz the agent's executable against the oracle."""
    oracle_path = "/app/oracle_ema"
    agent_path = "/home/user/ema_filter"

    assert os.path.exists(oracle_path), f"Oracle missing: {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle not executable: {oracle_path}"

    random.seed(42)
    num_tests = 100

    for i in range(num_tests):
        # Random number of floats between 1 and 1024 (4 to 4096 bytes)
        num_floats = random.randint(1, 1024)

        # Generate random floats
        # Use a mix of normal ranges, negatives, and zeros to avoid NaNs but test logic
        input_floats = [random.uniform(-1000.0, 1000.0) for _ in range(num_floats)]
        input_bytes = struct.pack(f"<{num_floats}f", *input_floats)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_bytes,
            capture_output=True,
            timeout=2
        )
        assert oracle_proc.returncode == 0, "Oracle failed to execute."
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=input_bytes,
            capture_output=True,
            timeout=2
        )
        assert agent_proc.returncode == 0, f"Agent program failed with return code {agent_proc.returncode}."
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            # Try to unpack to show a better error message if lengths match
            if len(oracle_out) == len(agent_out) and len(oracle_out) % 4 == 0:
                oracle_floats = struct.unpack(f"<{len(oracle_out)//4}f", oracle_out)
                agent_floats = struct.unpack(f"<{len(agent_out)//4}f", agent_out)

                # Find the first mismatch
                for idx, (o_val, a_val) in enumerate(zip(oracle_floats, agent_floats)):
                    if o_val != a_val:
                        pytest.fail(
                            f"Output mismatch at float index {idx}.\n"
                            f"Input float at index {idx}: {input_floats[idx]}\n"
                            f"Expected output: {o_val}\n"
                            f"Agent output: {a_val}"
                        )
            else:
                pytest.fail(
                    f"Output byte length mismatch.\n"
                    f"Expected {len(oracle_out)} bytes, got {len(agent_out)} bytes."
                )