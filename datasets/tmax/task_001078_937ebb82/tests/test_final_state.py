# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/opt/oracle/welford_cli"
AGENT_PATH = "/home/user/fixed_welford_cli"
N_ITERATIONS = 100

def test_fixed_binary_exists():
    assert os.path.isfile(AGENT_PATH), f"The fixed binary was not found at {AGENT_PATH}."
    assert os.access(AGENT_PATH, os.X_OK), f"The file at {AGENT_PATH} is not executable."

@pytest.mark.parametrize("i", range(N_ITERATIONS))
def test_fuzz_equivalence(i):
    random.seed(42 + i)

    L = random.randint(1000, 100_000)
    floats = [str(random.uniform(-1_000_000.0, 1_000_000.0)) for _ in range(L)]
    input_data = "\n".join(floats).encode('utf-8') + b"\n"

    oracle_proc = subprocess.run(
        [ORACLE_PATH],
        input=input_data,
        capture_output=True,
        check=False
    )
    assert oracle_proc.returncode == 0, f"Oracle failed to execute on iteration {i}."

    agent_proc = subprocess.run(
        [AGENT_PATH],
        input=input_data,
        capture_output=True,
        check=False
    )

    assert agent_proc.returncode == 0, (
        f"Agent binary failed to execute on iteration {i}. "
        f"STDERR: {agent_proc.stderr.decode('utf-8', errors='replace')}"
    )

    if agent_proc.stdout != oracle_proc.stdout:
        # We don't want to dump 100k lines to the console, so we provide a summary
        oracle_lines = oracle_proc.stdout.splitlines()
        agent_lines = agent_proc.stdout.splitlines()

        diff_idx = -1
        for idx, (oline, aline) in enumerate(zip(oracle_lines, agent_lines)):
            if oline != aline:
                diff_idx = idx
                break

        if diff_idx == -1 and len(oracle_lines) != len(agent_lines):
            diff_idx = min(len(oracle_lines), len(agent_lines))

        pytest.fail(
            f"Output mismatch on fuzz iteration {i} at line {diff_idx + 1}.\n"
            f"Input float at this line: {floats[diff_idx] if diff_idx < len(floats) else 'N/A'}\n"
            f"Expected (Oracle): {oracle_lines[diff_idx].decode('utf-8', errors='replace') if diff_idx < len(oracle_lines) else 'EOF'}\n"
            f"Got (Agent):       {agent_lines[diff_idx].decode('utf-8', errors='replace') if diff_idx < len(agent_lines) else 'EOF'}"
        )