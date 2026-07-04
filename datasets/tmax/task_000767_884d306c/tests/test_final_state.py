# test_final_state.py
import os
import random
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/legacy_encoder"
AGENT_PATH = "/home/user/encoder_impl"
NUM_ITERATIONS = 200

def test_agent_program_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent program not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent program {AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent program {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle program not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle program {ORACLE_PATH} is not executable"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(NUM_ITERATIONS):
            length = random.randint(10, 5000)
            input_data = bytes(random.choices(range(256), k=length))

            input_file = os.path.join(tmpdir, f"input_{i}.bin")
            oracle_output_file = os.path.join(tmpdir, f"oracle_out_{i}.bin")
            agent_output_file = os.path.join(tmpdir, f"agent_out_{i}.bin")

            with open(input_file, "wb") as f:
                f.write(input_data)

            # Run oracle
            oracle_proc = subprocess.run(
                [ORACLE_PATH, input_file, oracle_output_file],
                capture_output=True,
                text=True
            )
            assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i} with stderr: {oracle_proc.stderr}"

            # Run agent
            agent_proc = subprocess.run(
                [AGENT_PATH, input_file, agent_output_file],
                capture_output=True,
                text=True
            )
            assert agent_proc.returncode == 0, f"Agent program failed on iteration {i} with stderr: {agent_proc.stderr}"

            # Read outputs
            with open(oracle_output_file, "rb") as f:
                oracle_output = f.read()

            with open(agent_output_file, "rb") as f:
                agent_output = f.read()

            if oracle_output != agent_output:
                # Truncate output for error message if it's too long
                trunc_len = 100
                in_hex = input_data[:trunc_len].hex() + ("..." if len(input_data) > trunc_len else "")
                or_hex = oracle_output[:trunc_len].hex() + ("..." if len(oracle_output) > trunc_len else "")
                ag_hex = agent_output[:trunc_len].hex() + ("..." if len(agent_output) > trunc_len else "")

                pytest.fail(
                    f"Mismatch on iteration {i} (input length {length}).\n"
                    f"Input (hex): {in_hex}\n"
                    f"Oracle output (hex): {or_hex}\n"
                    f"Agent output (hex): {ag_hex}"
                )