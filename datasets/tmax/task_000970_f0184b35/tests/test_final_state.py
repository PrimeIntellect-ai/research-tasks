# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/oracle"
AGENT_SCRIPT = "/home/user/solution.sh"
N_ITERATIONS = 500

def generate_random_bytes(length: int) -> bytes:
    """Generate a random sequence of bytes of the given length."""
    return bytes(random.choices(range(256), k=length))

def test_solution_exists():
    """Ensure the agent created the solution script."""
    assert os.path.exists(AGENT_SCRIPT), f"Solution script missing at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"Solution path {AGENT_SCRIPT} is not a file"

def test_fuzz_equivalence():
    """Fuzz the agent's script against the oracle binary."""
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"

    # Use a fixed seed for reproducibility
    random.seed(42)

    for i in range(N_ITERATIONS):
        length = random.randint(1, 256)
        input_data = generate_random_bytes(length)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on iteration {i} with input length {length}.")

        # Run agent script
        try:
            agent_proc = subprocess.run(
                ["bash", AGENT_SCRIPT],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on iteration {i} with input length {length}.")

        if oracle_out != agent_out:
            # Truncate hex output for display if it's too long, but keep enough for debugging
            disp_input = input_data.hex()
            disp_oracle = oracle_out.hex()
            disp_agent = agent_out.hex()

            if len(disp_input) > 100: disp_input = disp_input[:100] + "..."
            if len(disp_oracle) > 100: disp_oracle = disp_oracle[:100] + "..."
            if len(disp_agent) > 100: disp_agent = disp_agent[:100] + "..."

            pytest.fail(
                f"Mismatch on iteration {i} with input length {length}.\n"
                f"Input (hex): {disp_input}\n"
                f"Oracle output (hex): {disp_oracle}\n"
                f"Agent output (hex): {disp_agent}\n"
                f"Oracle stderr: {oracle_proc.stderr.decode(errors='replace')}\n"
                f"Agent stderr: {agent_proc.stderr.decode(errors='replace')}"
            )