# test_final_state.py
import os
import subprocess
import base64
import random
import string
import pytest

ORACLE_PATH = "/opt/oracle/analyze_oracle"
AGENT_SCRIPT = "/home/user/analyze.py"
PYTHON_BIN = "/usr/bin/python3"

def generate_fuzz_inputs(n=100, seed=42):
    random.seed(seed)
    inputs = []
    for _ in range(n):
        if random.random() < 0.9:
            # Valid base64
            length = random.randint(10, 1000)
            raw_bytes = bytes(random.getrandbits(8) for _ in range(length))
            b64_str = base64.b64encode(raw_bytes).decode('utf-8')
            inputs.append(b64_str)
        else:
            # Invalid base64
            length = random.randint(10, 100)
            bad_chars = "!@#$%^&*()_+"
            b64_str = "".join(random.choice(string.ascii_letters + string.digits + bad_chars) for _ in range(length))
            inputs.append(b64_str)
    return inputs

def test_agent_script_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle {ORACLE_PATH} missing."
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle {ORACLE_PATH} not executable."

    inputs = generate_fuzz_inputs(100)

    for idx, inp in enumerate(inputs):
        # Run oracle
        try:
            oracle_res = subprocess.run(
                [ORACLE_PATH, inp],
                capture_output=True,
                text=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {idx}")

        # Run agent
        try:
            agent_res = subprocess.run(
                [PYTHON_BIN, AGENT_SCRIPT, inp],
                capture_output=True,
                text=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input {idx}")

        assert agent_res.returncode == oracle_res.returncode, (
            f"Return code mismatch on input {idx}.\n"
            f"Input: {inp[:50]}...\n"
            f"Oracle RC: {oracle_res.returncode}, Agent RC: {agent_res.returncode}\n"
            f"Oracle stdout: {oracle_res.stdout}\n"
            f"Agent stdout: {agent_res.stdout}\n"
            f"Agent stderr: {agent_res.stderr}"
        )

        assert agent_res.stdout == oracle_res.stdout, (
            f"Stdout mismatch on input {idx}.\n"
            f"Input: {inp[:50]}...\n"
            f"Oracle stdout: {repr(oracle_res.stdout)}\n"
            f"Agent stdout: {repr(agent_res.stdout)}"
        )