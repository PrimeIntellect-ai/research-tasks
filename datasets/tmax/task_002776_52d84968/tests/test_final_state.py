# test_final_state.py

import os
import random
import subprocess
import pytest

def test_agent_program_exists():
    agent_prog = "/home/user/encoder"
    assert os.path.exists(agent_prog), f"Agent program {agent_prog} does not exist."
    assert os.path.isfile(agent_prog), f"{agent_prog} is not a file."
    assert os.access(agent_prog, os.X_OK), f"{agent_prog} is not executable."

def test_fuzz_equivalence():
    oracle_prog = "/app/legacy_asset_encoder"
    agent_prog = "/home/user/encoder"

    assert os.path.exists(oracle_prog), f"Oracle program {oracle_prog} is missing."
    assert os.access(oracle_prog, os.X_OK), f"Oracle program {oracle_prog} is not executable."

    # Use a fixed seed for reproducibility
    rng = random.Random(42)

    # 1000 iterations
    for i in range(1000):
        # Random length between 0 and 8192
        length = rng.randint(0, 8192)

        # Generate random bytes
        input_data = bytearray(rng.getrandbits(8) for _ in range(length))

        # Run oracle
        env = os.environ.copy()
        env.pop("WS_PORT", None) # Ensure WS_PORT is unset

        try:
            oracle_proc = subprocess.run(
                [oracle_prog],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle program timed out on iteration {i} (length {length})")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_prog],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on iteration {i} (length {length})")

        # Assert equivalence
        if oracle_out != agent_out:
            # Provide a helpful error message but don't dump 8KB of binary to console directly
            err_msg = (
                f"Output mismatch on iteration {i} (input length {length}).\n"
                f"Oracle output length: {len(oracle_out)}, Agent output length: {len(agent_out)}\n"
            )
            if len(input_data) < 64:
                err_msg += f"Input data (hex): {input_data.hex()}\n"
                err_msg += f"Oracle out (hex): {oracle_out.hex()}\n"
                err_msg += f"Agent out (hex):  {agent_out.hex()}"
            pytest.fail(err_msg)