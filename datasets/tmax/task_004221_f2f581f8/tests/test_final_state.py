# test_final_state.py

import os
import subprocess
import random
import pytest
import json

def test_ci_verify_script_exists():
    path = "/home/user/ci_verify.sh"
    assert os.path.isfile(path), f"Missing CI script: {path}"
    assert os.access(path, os.X_OK), f"CI script is not executable: {path}"

def test_build_result_log_exists_and_valid():
    # If the user ran their own ci_verify.sh, the log should exist.
    # If not, we can at least check if it's there or run it ourselves.
    # The prompt says the verifier will execute it, but we can just check if it exists or run it.
    script_path = "/home/user/ci_verify.sh"
    log_path = "/home/user/build_result.log"

    if not os.path.exists(log_path):
        # Try running it
        subprocess.run([script_path], cwd="/home/user", timeout=15)

    assert os.path.isfile(log_path), f"Missing build result log: {log_path}"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
        assert isinstance(data, dict), "Log content is not a JSON object"
    except json.JSONDecodeError:
        pytest.fail(f"Build result log does not contain valid JSON: {content[:100]}")

def test_fuzz_equivalence_checksum():
    oracle_path = "/app/oracle/checksum_reference.bin"
    agent_path = "/home/user/build_tools/checksum_standalone"

    assert os.path.isfile(oracle_path), f"Missing oracle: {oracle_path}"
    assert os.path.isfile(agent_path), f"Missing agent executable: {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent executable not executable: {agent_path}"

    random.seed(42)

    # Run 50 iterations with varying sizes to prevent test timeout but ensure coverage
    sizes = [random.randint(10, 1000) for _ in range(40)] + \
            [random.randint(1000, 100000) for _ in range(8)] + \
            [random.randint(100000, 1000000) for _ in range(2)]

    for i, size in enumerate(sizes):
        input_data = bytes(random.getrandbits(8) for _ in range(size))

        # Run oracle
        proc_oracle = subprocess.run(
            [oracle_path],
            input=input_data,
            capture_output=True,
            timeout=5
        )
        assert proc_oracle.returncode == 0, f"Oracle failed on input {i} (size {size})"
        oracle_out = proc_oracle.stdout.strip()

        # Run agent
        proc_agent = subprocess.run(
            [agent_path],
            input=input_data,
            capture_output=True,
            timeout=5
        )
        assert proc_agent.returncode == 0, f"Agent failed on input {i} (size {size})\nStderr: {proc_agent.stderr.decode(errors='ignore')}"
        agent_out = proc_agent.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on input {i} (size {size}).\n"
            f"Oracle: {oracle_out}\n"
            f"Agent:  {agent_out}"
        )