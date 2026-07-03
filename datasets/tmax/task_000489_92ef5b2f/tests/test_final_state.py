# test_final_state.py

import os
import subprocess
import random
import json
import urllib.request
import socket
import pytest

def generate_fuzz_inputs(n=1000, seed=42):
    random.seed(seed)
    inputs = []
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-/:?=&"

    for _ in range(n):
        if random.random() < 0.5:
            # Generate valid-looking inputs
            service = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-", k=random.randint(1, 20)))
            method = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-", k=random.randint(1, 20)))
            bench = str(random.randint(0, 9999))
            retry = str(random.randint(0, 99))
            inp = f"test-env://{service}/{method}?bench={bench}&retry={retry}"

            # Introduce malformed mutations
            mutation_choice = random.random()
            if mutation_choice < 0.05:
                inp = inp.replace("test-env://", "test-env:/")
            elif mutation_choice < 0.10:
                inp = inp.replace(f"bench={bench}", "bench=abc")
            elif mutation_choice < 0.15:
                inp = inp.replace("?", "&")
        else:
            # Generate completely random junk within charset
            inp = "".join(random.choices(charset, k=random.randint(10, 150)))

        inputs.append(inp)
    return inputs

def test_fuzz_parser():
    agent_bin = "/home/user/app/build/url_parser"
    oracle_bin = "/home/user/oracle/url_parser_oracle"

    assert os.path.exists(agent_bin), f"Agent binary not found at {agent_bin}. Did you run 'make parser'?"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable."

    inputs = generate_fuzz_inputs(1000)

    for inp in inputs:
        agent_proc = subprocess.run([agent_bin], input=inp.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        oracle_proc = subprocess.run([oracle_bin], input=inp.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Output mismatch on input: {inp}\n"
            f"Oracle stdout: {oracle_proc.stdout}\n"
            f"Agent stdout: {agent_proc.stdout}"
        )

def test_services_running():
    def is_port_open(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(('127.0.0.1', port)) == 0

    assert is_port_open(6379), "Redis server is not listening on port 6379."
    assert is_port_open(50051), "Python mock gRPC server is not listening on port 50051."
    assert is_port_open(8080), "Gateway service is not listening on port 8080."

def test_end_to_end_gateway():
    url = "http://localhost:8080/benchmark"
    payload = b"test-env://checkout/process?bench=25&retry=1"
    req = urllib.request.Request(url, data=payload, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            response_body = response.read().decode('utf-8')
            data = json.loads(response_body)

            assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
            assert data.get("service") == "checkout", f"Expected service 'checkout', got {data.get('service')}"
            assert data.get("method") == "process", f"Expected method 'process', got {data.get('method')}"
            assert data.get("bench_simulated_ms") == 25, f"Expected bench_simulated_ms 25, got {data.get('bench_simulated_ms')}"
            assert "redis_count" in data, "Expected 'redis_count' in response JSON"
            assert isinstance(data["redis_count"], int) and data["redis_count"] > 0, "Expected 'redis_count' to be a positive integer"

    except urllib.error.URLError as e:
        pytest.fail(f"End-to-end request failed: {e}")
    except json.JSONDecodeError:
        pytest.fail(f"Failed to decode JSON from gateway response: {response_body}")