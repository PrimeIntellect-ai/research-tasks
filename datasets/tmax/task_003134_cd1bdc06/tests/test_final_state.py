# test_final_state.py

import os
import subprocess
import random
import pytest

def test_eqm_util_built_and_correct():
    binary_path = "/app/email_quota_monitor-1.2.0/build/eqm_util"
    assert os.path.isfile(binary_path), f"Expected compiled binary at {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable."

    env = os.environ.copy()
    env["QUOTA_WARN_LEVEL"] = "85"

    try:
        result = subprocess.run(
            [binary_path],
            env=env,
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {binary_path} timed out.")

    assert "Warning Level: 85%" in result.stdout, (
        f"Expected output to contain 'Warning Level: 85%', but got stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

def test_wrapper_fuzz_equivalence():
    agent_bin = "/home/user/quota_wrapper"
    oracle_bin = "/opt/legacy/quota_oracle"

    assert os.path.isfile(agent_bin), f"Agent binary {agent_bin} does not exist."
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable."
    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} does not exist."
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable."

    random.seed(42)
    N = 1000
    inputs = [str(random.randint(0, 5000000)) for _ in range(N)]
    input_str = "\n".join(inputs) + "\n"

    try:
        oracle_result = subprocess.run(
            [oracle_bin],
            input=input_str,
            capture_output=True,
            text=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle binary timed out.")

    try:
        agent_result = subprocess.run(
            [agent_bin],
            input=input_str,
            capture_output=True,
            text=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Agent binary timed out.")

    oracle_lines = oracle_result.stdout.strip().split('\n')
    agent_lines = agent_result.stdout.strip().split('\n')

    assert len(agent_lines) == len(oracle_lines), (
        f"Line count mismatch. Oracle produced {len(oracle_lines)} lines, agent produced {len(agent_lines)} lines."
    )

    for i, (oracle_line, agent_line) in enumerate(zip(oracle_lines, agent_lines)):
        assert oracle_line == agent_line, (
            f"Output mismatch on input {inputs[i]}.\n"
            f"Oracle output: {oracle_line}\n"
            f"Agent output:  {agent_line}\n"
            f"Line number:   {i+1}"
        )