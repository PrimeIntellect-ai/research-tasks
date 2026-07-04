# test_final_state.py

import os
import random
import string
import struct
import subprocess
import pytest

def test_gateway_env():
    """Verify that the gateway .env file is correctly configured."""
    env_path = "/app/gateway/.env"
    assert os.path.isfile(env_path), f"Gateway .env file missing at {env_path}"

    with open(env_path, "r") as f:
        content = f.read()

    assert "GATEWAY_PORT=8080" in content, "GATEWAY_PORT is not correctly set in .env"
    assert "WORKER_ADDR=127.0.0.1:9000" in content, "WORKER_ADDR is not correctly set in .env"

def test_worker_daemon_compiled():
    """Verify that worker_daemon is compiled and executable."""
    daemon_path = "/app/c_worker/worker_daemon"
    assert os.path.isfile(daemon_path), f"worker_daemon not found at {daemon_path}"
    assert os.access(daemon_path, os.X_OK), f"worker_daemon at {daemon_path} is not executable"

def test_transformer_fuzz_equivalence():
    """Verify that the transformer binary perfectly matches the oracle on 1000 random inputs."""
    agent_bin = "/app/c_worker/transformer"
    oracle_bin = "/app/reference/transformer_oracle"

    assert os.path.isfile(agent_bin), f"transformer binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"transformer at {agent_bin} is not executable"

    assert os.path.isfile(oracle_bin), f"oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"oracle at {oracle_bin} is not executable"

    random.seed(42)
    printable_chars = string.ascii_letters + string.digits + string.punctuation + " "

    for i in range(1000):
        L = random.randint(1, 4096)
        ascii_data = "".join(random.choices(printable_chars, k=L)).encode("ascii")
        payload = struct.pack("<I", L) + ascii_data

        try:
            oracle_proc = subprocess.run([oracle_bin], input=payload, capture_output=True, timeout=2)
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle binary timed out on iteration {i} with input length {L}")

        try:
            agent_proc = subprocess.run([agent_bin], input=payload, capture_output=True, timeout=2)
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on iteration {i} with input length {L}")

        if agent_out != oracle_out:
            pytest.fail(
                f"Mismatch on iteration {i} (input length {L}).\n"
                f"Input payload (first 50 bytes): {payload[:50]!r}...\n"
                f"Expected output (first 50 bytes): {oracle_out[:50]!r}...\n"
                f"Agent output (first 50 bytes): {agent_out[:50]!r}..."
            )