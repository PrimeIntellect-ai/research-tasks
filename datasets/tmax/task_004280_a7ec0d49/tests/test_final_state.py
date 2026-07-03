# test_final_state.py
import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/telemetry_obfuscator"
AGENT_PATH = "/home/user/py_obfuscator.py"
NUM_TESTS = 500
MAX_LEN = 2048

def test_agent_script_exists():
    assert os.path.exists(AGENT_PATH), f"Agent script not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Path {AGENT_PATH} is not a file"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable"

    random.seed(42)

    for i in range(NUM_TESTS):
        length = random.randint(0, MAX_LEN)
        input_data = bytes(random.choices(range(256), k=length))

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_data,
            capture_output=True,
            check=False
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on test {i} with length {length}"
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            ["python3", AGENT_PATH],
            input=input_data,
            capture_output=True,
            check=False
        )
        assert agent_proc.returncode == 0, f"Agent script failed on test {i} with length {length}. Stderr: {agent_proc.stderr.decode(errors='replace')}"
        agent_output = agent_proc.stdout

        if oracle_output != agent_output:
            # Provide a clear failure message
            input_hex = input_data.hex()
            if len(input_hex) > 100:
                input_hex = input_hex[:100] + "... (truncated)"

            oracle_hex = oracle_output.hex()
            if len(oracle_hex) > 100:
                oracle_hex = oracle_hex[:100] + "... (truncated)"

            agent_hex = agent_output.hex()
            if len(agent_hex) > 100:
                agent_hex = agent_hex[:100] + "... (truncated)"

            pytest.fail(
                f"Mismatch on test {i} (length {length}):\n"
                f"Input (hex): {input_hex}\n"
                f"Oracle output (hex): {oracle_hex}\n"
                f"Agent output (hex):  {agent_hex}\n"
            )