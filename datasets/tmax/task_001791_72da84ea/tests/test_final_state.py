# test_final_state.py
import os
import subprocess
import random
import string
import pytest

AGENT_PATH = "/home/user/compress_rotate"
ORACLE_PATH = "/app/oracle_compress"

def test_agent_executable_exists():
    """Verify that the agent's compressor executable exists and is executable."""
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent file at {AGENT_PATH} is not executable"

def test_oracle_exists():
    """Verify that the oracle executable exists and is executable."""
    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle file at {ORACLE_PATH} is not executable"

def generate_test_cases():
    """Generate 500 test cases based on the fuzz distribution and edge cases."""
    random.seed(42)
    cases = []

    # Edge cases
    cases.append("")
    cases.append("^" * 5000)
    cases.append("a" * 5000)
    cases.append("a^" * 2500)
    cases.append("^^" * 2500)

    # Runs around MIN_RUN (6)
    for c in ['a', '^']:
        for i in range(1, 10):
            cases.append(c * i)

    chars = string.printable

    # Random fuzz cases to reach N=500 total
    for _ in range(477):
        length = random.randint(0, 10000)
        parts = []
        curr = 0
        while curr < length:
            r = random.random()
            if r < 0.2:
                # Run of escape characters
                l = random.randint(1, 15)
                parts.append('^' * l)
                curr += l
            elif r < 0.5:
                # Run of a random character
                c = random.choice(chars)
                l = random.randint(1, 15)
                parts.append(c * l)
                curr += l
            else:
                # Random mixed characters
                l = random.randint(1, 50)
                parts.append(''.join(random.choices(chars, k=l)))
                curr += l
        cases.append("".join(parts)[:length])

    return cases

@pytest.mark.parametrize("input_data", generate_test_cases())
def test_fuzz_equivalence(input_data):
    """Run both the oracle and the agent's program on random inputs and assert exact equivalence."""
    if not os.path.isfile(AGENT_PATH) or not os.access(AGENT_PATH, os.X_OK):
        pytest.fail(f"Agent executable not found or not executable at {AGENT_PATH}")

    input_bytes = input_data.encode('utf-8')

    # Run oracle
    oracle_proc = subprocess.run(
        [ORACLE_PATH],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5
    )
    assert oracle_proc.returncode == 0, f"Oracle failed: {oracle_proc.stderr.decode('utf-8', errors='replace')}"

    # Run agent
    agent_proc = subprocess.run(
        [AGENT_PATH],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5
    )
    assert agent_proc.returncode == 0, f"Agent failed: {agent_proc.stderr.decode('utf-8', errors='replace')}"

    # Compare outputs
    if oracle_proc.stdout != agent_proc.stdout:
        in_str = input_data if len(input_data) < 100 else input_data[:100] + "... (truncated)"
        or_str = oracle_proc.stdout.decode('utf-8', errors='replace')
        or_str = or_str if len(or_str) < 100 else or_str[:100] + "... (truncated)"
        ag_str = agent_proc.stdout.decode('utf-8', errors='replace')
        ag_str = ag_str if len(ag_str) < 100 else ag_str[:100] + "... (truncated)"

        pytest.fail(
            f"Output mismatch!\n"
            f"Input: {repr(in_str)}\n"
            f"Expected (Oracle): {repr(or_str)}\n"
            f"Got (Agent): {repr(ag_str)}"
        )