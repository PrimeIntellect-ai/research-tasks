# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/opt/oracle/doctar_oracle"
AGENT_PATH = "/app/doctar-1.0/doctar_sanitize"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"

    random.seed(42)
    N = 10000
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/."

    # Generate test cases
    test_cases = []
    for _ in range(N):
        length = random.randint(0, 256)
        test_case = ''.join(random.choice(charset) for _ in range(length))
        test_cases.append(test_case)

    # Add some specific edge cases
    test_cases.extend([
        "",
        ".",
        "..",
        "/",
        "//",
        "///",
        "/./.././/..",
        "a/b/c/../../d",
        "a//b/../c/./d"
    ])

    for i, test_case in enumerate(test_cases):
        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH, test_case],
                capture_output=True,
                text=True,
                timeout=1
            )
            oracle_stdout = oracle_proc.stdout
            oracle_stderr = oracle_proc.stderr
            oracle_rc = oracle_proc.returncode
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {repr(test_case)}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_PATH, test_case],
                capture_output=True,
                text=True,
                timeout=1
            )
            agent_stdout = agent_proc.stdout
            agent_stderr = agent_proc.stderr
            agent_rc = agent_proc.returncode
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on input: {repr(test_case)}")

        # Check equivalence
        assert agent_rc == oracle_rc, (
            f"Return code mismatch on input {repr(test_case)}.\n"
            f"Oracle returned {oracle_rc}, Agent returned {agent_rc}."
        )
        assert agent_stdout == oracle_stdout, (
            f"Stdout mismatch on input {repr(test_case)}.\n"
            f"Oracle stdout: {repr(oracle_stdout)}\n"
            f"Agent stdout: {repr(agent_stdout)}"
        )