# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

ORACLE_PATH = "/app/wal_packer"
AGENT_SCRIPT = "/home/user/wal_packer.py"

def generate_random_binary(size):
    """Generate random binary data with some repeating sequences and 0xAA bytes to trigger RLE."""
    if size == 0:
        return b""

    out = bytearray()
    while len(out) < size:
        choice = random.random()
        if choice < 0.1:
            # Insert 0xAA
            out.append(0xAA)
        elif choice < 0.3:
            # Insert repeating sequence
            repeat_byte = random.randint(0, 255)
            repeat_count = random.randint(3, 300)
            out.extend([repeat_byte] * repeat_count)
        else:
            # Insert random bytes
            out.extend(random.randbytes(min(100, size - len(out))))

    return bytes(out[:size])

def test_agent_script_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} missing."
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} missing."

    random.seed(42)

    # Generate a mix of sizes
    sizes = [0, 1, 2, 3, 10, 255, 256, 1024, 10000, 50000, 100000]
    # Add some random sizes
    sizes += [random.randint(10, 100000) for _ in range(40)]

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, size in enumerate(sizes):
            input_file = os.path.join(tmpdir, f"input_{i}.wal")
            oracle_out = os.path.join(tmpdir, f"oracle_out_{i}.pack")
            agent_out = os.path.join(tmpdir, f"agent_out_{i}.pack")

            data = generate_random_binary(size)
            with open(input_file, "wb") as f:
                f.write(data)

            # Run oracle
            oracle_proc = subprocess.run(
                [ORACLE_PATH, input_file, oracle_out],
                capture_output=True
            )
            assert oracle_proc.returncode == 0, f"Oracle failed on input {i} (size {size})"

            # Run agent
            agent_proc = subprocess.run(
                ["python3", AGENT_SCRIPT, input_file, agent_out],
                capture_output=True
            )
            assert agent_proc.returncode == 0, f"Agent script failed on input {i} (size {size}). Stderr: {agent_proc.stderr.decode(errors='replace')}"

            # Compare outputs
            assert os.path.exists(oracle_out), f"Oracle output missing for input {i}"
            assert os.path.exists(agent_out), f"Agent output missing for input {i}"

            with open(oracle_out, "rb") as f:
                oracle_data = f.read()
            with open(agent_out, "rb") as f:
                agent_data = f.read()

            if oracle_data != agent_data:
                # Find first mismatch
                min_len = min(len(oracle_data), len(agent_data))
                mismatch_idx = -1
                for j in range(min_len):
                    if oracle_data[j] != agent_data[j]:
                        mismatch_idx = j
                        break
                if mismatch_idx == -1:
                    mismatch_idx = min_len

                pytest.fail(
                    f"Mismatch on input {i} (size {size}).\n"
                    f"Oracle output length: {len(oracle_data)}\n"
                    f"Agent output length: {len(agent_data)}\n"
                    f"First difference at byte {mismatch_idx}."
                )