# test_final_state.py
import os
import subprocess
import random
import string
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_sanitizer"
    agent_path = "/app/path_sanitizer-1.0.0/target/debug/path_sanitizer"
    base_dir = "/var/www/uploads"

    assert os.path.exists(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary is not executable"

    # Seed for reproducibility
    random.seed(42)

    # Alphabet based on truth distribution
    # Note: literal null bytes cannot be passed as POSIX command line arguments,
    # so we use '\\0' (backslash zero) and '%00' to represent null bytes in the payload.
    alphabet = list(string.ascii_letters + string.digits) + ['/', '.', '%2e', '%2f', '%00', '\\0', '<', '>']

    N = 10000
    for _ in range(N):
        length = random.randint(1, 256)
        payload = "".join(random.choices(alphabet, k=length))

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_path, base_dir, payload],
                capture_output=True,
                text=False,
                timeout=2
            )
            oracle_stdout = oracle_res.stdout
            oracle_stderr = oracle_res.stderr
            oracle_code = oracle_res.returncode
        except Exception as e:
            pytest.fail(f"Oracle failed to run on input {repr(payload)}: {e}")

        # Run agent
        try:
            agent_res = subprocess.run(
                [agent_path, base_dir, payload],
                capture_output=True,
                text=False,
                timeout=2
            )
            agent_stdout = agent_res.stdout
            agent_stderr = agent_res.stderr
            agent_code = agent_res.returncode
        except Exception as e:
            pytest.fail(f"Agent failed to run on input {repr(payload)}: {e}")

        assert agent_stdout == oracle_stdout, f"Stdout mismatch on input {repr(payload)}. Oracle: {repr(oracle_stdout)}, Agent: {repr(agent_stdout)}"
        assert agent_stderr == oracle_stderr, f"Stderr mismatch on input {repr(payload)}. Oracle: {repr(oracle_stderr)}, Agent: {repr(agent_stderr)}"
        assert agent_code == oracle_code, f"Return code mismatch on input {repr(payload)}. Oracle: {oracle_code}, Agent: {agent_code}"