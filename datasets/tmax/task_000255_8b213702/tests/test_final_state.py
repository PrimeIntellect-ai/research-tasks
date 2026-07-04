# test_final_state.py
import os
import subprocess
import random
import urllib.request
import urllib.error
import pytest
import json

def test_math_worker_exists_and_executable():
    path = "/home/user/math_worker.sh"
    assert os.path.isfile(path), f"Agent script {path} does not exist"
    assert os.access(path, os.X_OK), f"Agent script {path} is not executable"

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_oracle"
    agent_path = "/home/user/math_worker.sh"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} missing"
    assert os.path.isfile(agent_path), f"Agent script {agent_path} missing"

    random.seed(42)

    for _ in range(500):
        major = random.randint(0, 20)
        minor = random.randint(0, 20)
        patch = random.randint(0, 20)
        semver = f"{major}.{minor}.{patch}"
        n = random.randint(1, 10000)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path, semver, str(n)],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {semver} {n}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["bash", agent_path, semver, str(n)],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input {semver} {n}. Stderr: {agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input '{semver}' '{n}'. "
            f"Oracle output: '{oracle_out}', Agent output: '{agent_out}'"
        )

def test_end_to_end_api():
    # Test the full flow through Nginx -> Flask -> bash script -> Redis
    v = "2.4.1"
    n = 42
    url = f"http://127.0.0.1:8080/api/math?v={v}&n={n}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8').strip()
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 or Flask on 5000: {e}")

    assert status == 200, f"Expected HTTP 200, got {status}"

    # 2.4.1 and 42 -> 2*100 + 4*10 + 1 + 42*3 = 241 + 126 = 367
    expected_result = "367"
    assert body == expected_result, f"Expected API to return '{expected_result}', got '{body}'"

def test_redis_caching():
    # Verify that the previous request populated Redis
    # The cache key is "v:n" -> "2.4.1:42"
    import socket

    # Simple redis check without redis-py to avoid dependency issues if environment is slightly different
    # But since we can assume standard library, we'll send a raw RESP command
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect(('127.0.0.1', 6379))
        cmd = "*2\r\n$3\r\nGET\r\n$8\r\n2.4.1:42\r\n"
        sock.sendall(cmd.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')
        sock.close()

        # RESP bulk string format: $3\r\n367\r\n
        assert "367" in response, f"Expected cached value '367' in Redis for key '2.4.1:42', got raw response: {response}"
    except Exception as e:
        pytest.fail(f"Failed to verify Redis cache: {e}")