# test_final_state.py

import os
import time
import pytest
import urllib.request
import urllib.error

def test_correctness():
    """Test that the checksum endpoint returns the correct CRC32C for a known payload."""
    data = b"hello world"
    req = urllib.request.Request("http://127.0.0.1:8080/checksum", data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode("utf-8").strip()
            assert result == "3381945770", f"Expected checksum '3381945770', got '{result}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the Nginx proxy or backend: {e}")

def test_nginx_method_not_allowed():
    """Test that Nginx rejects non-POST requests to /checksum."""
    req = urllib.request.Request("http://127.0.0.1:8080/checksum", method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            pytest.fail(f"Expected HTTP 405 for GET request, but got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 405, f"Expected HTTP 405 Method Not Allowed, got {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx: {e}")

def test_nginx_body_size_limit():
    """Test that Nginx enforces the 5M client body size limit."""
    data = b"A" * (6 * 1024 * 1024)  # 6MB
    req = urllib.request.Request("http://127.0.0.1:8080/checksum", data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            pytest.fail(f"Expected HTTP 413 Payload Too Large, but got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 413, f"Expected HTTP 413 Payload Too Large, got {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx: {e}")

def test_performance_metric():
    """
    Measure the average latency to checksum 1MB payloads.
    The C library must be compiled with optimizations (-O3) to pass this threshold.
    """
    payload = b"A" * 1024 * 1024  # 1MB
    times = []

    # Warm-up request
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/checksum", data=payload, method="POST")
        with urllib.request.urlopen(req) as response:
            response.read()
    except Exception as e:
        pytest.fail(f"Warm-up request failed: {e}")

    # Benchmark
    for _ in range(50):
        start = time.time()
        req = urllib.request.Request("http://127.0.0.1:8080/checksum", data=payload, method="POST")
        try:
            with urllib.request.urlopen(req) as response:
                response.read()
        except Exception as e:
            pytest.fail(f"Benchmark request failed: {e}")
        times.append(time.time() - start)

    avg_latency_ms = (sum(times) / len(times)) * 1000
    threshold = 3.0

    assert avg_latency_ms <= threshold, (
        f"Performance metric failed: Average latency {avg_latency_ms:.2f} ms exceeds "
        f"the threshold of {threshold} ms. Ensure the C library is compiled with -O3 optimizations."
    )