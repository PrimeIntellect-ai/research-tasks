# test_final_state.py
import os
import random
import subprocess
import pytest

def test_math_vm_exists_and_executable():
    """Verify that the agent's VM program exists and is executable."""
    agent_path = "/home/user/math_vm"
    assert os.path.isfile(agent_path), f"Agent's VM program not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent's VM program at {agent_path} is not executable"

def test_fuzz_equivalence():
    """Fuzz test the agent's VM against the oracle VM."""
    oracle_path = "/app/oracle_vm"
    agent_path = "/home/user/math_vm"

    # Fixed seed for reproducibility
    random.seed(42)

    N = 1000
    for i in range(N):
        length = random.randint(0, 2048)
        input_data = bytes(random.choices(range(256), k=length))

        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=input_data,
                capture_output=True,
                timeout=2
            )
        except subprocess.TimeoutExpired:
            pytest.fail("Oracle program timed out.")

        try:
            agent_proc = subprocess.run(
                [agent_path],
                input=input_data,
                capture_output=True,
                timeout=2
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input of length {length}.")

        # Check standard output
        oracle_out = oracle_proc.stdout
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            input_hex = input_data.hex()
            display_hex = input_hex[:100] + "..." if len(input_hex) > 100 else input_hex
            pytest.fail(
                f"Output mismatch on random input {i} (length {length}).\n"
                f"Input (hex): {display_hex}\n"
                f"Oracle stdout: {oracle_out!r}\n"
                f"Agent stdout: {agent_out!r}"
            )