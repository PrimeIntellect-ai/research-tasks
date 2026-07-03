# test_final_state.py

import os
import json
import time
import asyncio
import pytest

def test_proxy_binary_exists():
    path = "/app/vendored/goproxy-1.0/proxy"
    assert os.path.isfile(path), f"Compiled proxy binary {path} is missing. Did you run 'go build -o proxy main.go'?"

def test_benchmark_results_structure():
    path = "/home/user/benchmark_results.json"
    assert os.path.isfile(path), f"Benchmark results file {path} is missing."

    with open(path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    expected_keys = {"total_requests", "successful_requests", "total_time_seconds", "requests_per_second"}
    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"Benchmark results missing keys: {missing_keys}"

@pytest.mark.asyncio
async def test_proxy_throughput_and_correctness():
    # We use raw asyncio sockets to blast the server without external dependencies
    async def fetch(url_path):
        try:
            reader, writer = await asyncio.open_connection('127.0.0.1', 8080)
            request = f"GET {url_path} HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n"
            writer.write(request.encode())
            await writer.drain()

            response = await reader.read()
            writer.close()
            await writer.wait_closed()

            if b"200 OK" in response:
                return True
            return False
        except Exception:
            return False

    num_requests = 5000
    start_time = time.time()

    tasks = [fetch("/factor?n=10403") for _ in range(num_requests)]
    results = await asyncio.gather(*tasks)

    duration = time.time() - start_time
    successful = sum(results)

    assert successful == num_requests, f"Only {successful}/{num_requests} requests succeeded. The proxy might be dropping connections or deadlocking."

    rps = num_requests / duration
    threshold = 2000.0

    assert rps >= threshold, f"Throughput too low: measured {rps:.2f} RPS, expected >= {threshold} RPS."