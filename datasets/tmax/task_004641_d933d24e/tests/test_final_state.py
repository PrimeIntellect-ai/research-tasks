# test_final_state.py

import os
import random
import subprocess
import tempfile
import pytest

def test_fuzz_equivalence():
    oracle = "/app/wal_archive_tool"
    agent = "/home/user/custom_archive_tool"

    assert os.path.exists(agent), f"Agent binary not found at {agent}"
    assert os.access(agent, os.X_OK), f"Agent binary is not executable at {agent}"
    assert os.path.exists(oracle), f"Oracle binary not found at {oracle}"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(100):
            # Generate length
            if i == 0:
                length = 0
            elif i < 10:
                length = random.randint(1, 1000)
            else:
                length = random.randint(1000, 500000)

            # Generate data
            data = bytearray()
            while len(data) < length:
                chunk_type = random.choice(['random', 'repeat', 'nulls', 'ascii'])
                if chunk_type == 'random':
                    l = min(length - len(data), random.randint(1, 100))
                    data.extend(random.getrandbits(8) for _ in range(l))
                elif chunk_type == 'repeat':
                    l = min(length - len(data), random.randint(1, 1000))
                    b = random.getrandbits(8)
                    data.extend([b] * l)
                elif chunk_type == 'nulls':
                    l = min(length - len(data), random.randint(1, 1000))
                    data.extend([0] * l)
                else:
                    l = min(length - len(data), random.randint(1, 100))
                    data.extend(random.randint(32, 126) for _ in range(l))

            input_path = os.path.join(tmpdir, f"input_{i}.bin")
            oracle_out = os.path.join(tmpdir, f"oracle_{i}.bin")
            agent_out = os.path.join(tmpdir, f"agent_{i}.bin")

            with open(input_path, "wb") as f:
                f.write(data)

            # Run oracle
            try:
                subprocess.run([oracle, input_path, oracle_out], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Oracle failed on input {i} (length {length}). This should not happen.")

            # Run agent
            try:
                res = subprocess.run([agent, input_path, agent_out], capture_output=True, text=True, timeout=10)
            except subprocess.TimeoutExpired:
                pytest.fail(f"Agent timed out on input {i} (length {length}).")

            assert res.returncode == 0, f"Agent failed with return code {res.returncode} on input {i} (length {length}).\nStderr: {res.stderr}"
            assert os.path.exists(agent_out), f"Agent did not create output file for input {i}"

            with open(oracle_out, "rb") as f:
                oracle_data = f.read()
            with open(agent_out, "rb") as f:
                agent_data = f.read()

            if oracle_data != agent_data:
                # Find first mismatch
                for j in range(min(len(oracle_data), len(agent_data))):
                    if oracle_data[j] != agent_data[j]:
                        pytest.fail(
                            f"Mismatch on input {i} (length {length}) at byte {j}.\n"
                            f"Oracle byte: {hex(oracle_data[j])}\n"
                            f"Agent byte: {hex(agent_data[j])}"
                        )
                pytest.fail(
                    f"Mismatch on input {i} (length {length}).\n"
                    f"Oracle output length: {len(oracle_data)}\n"
                    f"Agent output length: {len(agent_data)}"
                )