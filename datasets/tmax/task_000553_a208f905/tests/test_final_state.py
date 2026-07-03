# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_policy_report_content():
    """Verify the policy report contains the correct extracted payload and CWE ID."""
    report_path = "/home/user/policy_report.txt"
    assert os.path.exists(report_path), f"Missing policy report at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {report_path}, found {len(lines)}"
    assert lines[0] == "..%2f..%2f..%2fetc%2fshadow", f"Line 1 (payload) is incorrect. Got: {lines[0]}"
    assert lines[1] == "CWE-22", f"Line 2 (CWE ID) is incorrect. Got: {lines[1]}"

def test_sanitizer_binary_exists():
    """Verify the student compiled the sanitizer binary."""
    agent_path = "/home/user/sanitizer"
    assert os.path.exists(agent_path), f"Compiled binary not found at {agent_path}"
    assert os.path.isfile(agent_path), f"{agent_path} is not a file"
    assert os.access(agent_path, os.X_OK), f"Binary at {agent_path} is not executable"

def generate_fuzz_payload():
    """Generate a random Upload-Path payload based on the truth distribution."""
    length = random.randint(10, 1024)
    charset = string.ascii_letters + string.digits + "/\\.%-_"
    payload = "".join(random.choice(charset) for _ in range(length))

    # Inject mutations (url encoding variants, nested traversals, null bytes)
    mutations = ["....//", "%2e%2e%2f", "..\\/", "%00", "../", "..\\"]
    for _ in range(random.randint(0, 5)):
        if not payload:
            break
        idx = random.randint(0, len(payload))
        mut = random.choice(mutations)
        payload = payload[:idx] + mut + payload[idx:]

    return payload[:1024]

def test_fuzz_equivalence():
    """Fuzz the agent's sanitizer against the oracle to ensure bit-exact equivalence."""
    oracle_path = "/app/sanitizer_oracle"
    agent_path = "/home/user/sanitizer"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent binary missing at {agent_path}"

    random.seed(1337)
    # Using 1000 iterations to balance thoroughness with test execution time limits
    N = 1000 

    for i in range(N):
        payload = generate_fuzz_payload()
        # Construct a raw HTTP request
        http_request = f"POST /upload HTTP/1.1\r\nHost: example.com\r\nUpload-Path: {payload}\r\nContent-Length: 0\r\n\r\n"
        input_bytes = http_request.encode('utf-8')

        try:
            oracle_proc = subprocess.run([oracle_path], input=input_bytes, capture_output=True, timeout=2)
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            # If oracle times out, skip this payload
            continue

        try:
            agent_proc = subprocess.run([agent_path], input=input_bytes, capture_output=True, timeout=2)
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on fuzz iteration {i}.\nInput:\n{http_request}")

        assert oracle_out == agent_out, (
            f"Fuzz equivalence failed on iteration {i}!\n"
            f"Input HTTP Request:\n{http_request}\n"
            f"Oracle Output (hex): {oracle_out.hex()}\n"
            f"Agent Output (hex): {agent_out.hex()}\n"
            f"Oracle Output (raw): {oracle_out}\n"
            f"Agent Output (raw): {agent_out}"
        )