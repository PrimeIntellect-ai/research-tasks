# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import json
import time
import pytest

WORKSPACE_DIR = "/home/user/cache-node"

def test_benchmark_speedup():
    """
    Runs the Go benchmark and verifies that the CGO implementation is at least
    4.0x faster than the pure Go implementation.
    """
    cmd = ["go", "test", "-bench=BenchmarkHash", "-benchmem"]
    result = subprocess.run(cmd, cwd=WORKSPACE_DIR, capture_output=True, text=True)

    assert result.returncode == 0, f"Benchmark command failed. Stderr: {result.stderr}\nStdout: {result.stdout}"

    go_ns = None
    cgo_ns = None

    for line in result.stdout.splitlines():
        if "BenchmarkHashGo" in line:
            parts = line.split()
            if len(parts) >= 3:
                try:
                    go_ns = float(parts[2])
                except ValueError:
                    pass
        elif "BenchmarkHashCGO" in line:
            parts = line.split()
            if len(parts) >= 3:
                try:
                    cgo_ns = float(parts[2])
                except ValueError:
                    pass

    assert go_ns is not None, f"Could not find BenchmarkHashGo results in output:\n{result.stdout}"
    assert cgo_ns is not None, f"Could not find BenchmarkHashCGO results in output:\n{result.stdout}"
    assert cgo_ns > 0, "CGO benchmark time must be greater than 0"

    speedup = go_ns / cgo_ns
    assert speedup >= 4.0, f"Speedup is {speedup:.2f}x (Go: {go_ns} ns/op, CGO: {cgo_ns} ns/op). Expected >= 4.0x"

def test_nginx_proxy_and_rate_limiting():
    """
    Sends requests to the Nginx endpoint to ensure proxying works and
    rate limiting (5 req/s) is correctly applied by the Go service.
    """
    url = "http://localhost:8080/api/upload"
    data = json.dumps({"branch": "main", "size": 1000}).encode('utf-8')

    # Sleep briefly to ensure we have a fresh rate limit window
    time.sleep(1.5)

    responses = []

    for _ in range(8):
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            resp = urllib.request.urlopen(req, timeout=2)
            responses.append(resp.status)
        except urllib.error.HTTPError as e:
            responses.append(e.code)
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to Nginx at {url}: {e.reason}")
        except Exception as e:
            responses.append(str(e))

    # The first few requests should succeed (e.g., 200 OK), and subsequent requests
    # within the same second should hit the 429 Too Many Requests limit.
    assert 429 in responses, f"Expected HTTP 429 Too Many Requests, but got responses: {responses}. Rate limiting might not be working or Nginx is not proxying correctly."

    # Ensure at least one request succeeded or was processed by the Go app (not just 502s)
    # The Go app might return 200, 201, or 202 for a successful upload.
    successful_responses = [r for r in responses if isinstance(r, int) and 200 <= r < 300]
    assert len(successful_responses) > 0, f"Expected at least one successful request before rate limiting, got: {responses}"

def test_go_service_running_on_9000():
    """
    Verifies that the Go service is listening directly on port 9000.
    """
    url = "http://localhost:9000/api/upload"
    data = json.dumps({"branch": "main", "size": 1000}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        resp = urllib.request.urlopen(req, timeout=2)
        status = resp.status
    except urllib.error.HTTPError as e:
        status = e.code
    except urllib.error.URLError as e:
        pytest.fail(f"Go service is not listening on port 9000: {e.reason}")

    assert status in [200, 201, 202, 429], f"Unexpected status code from Go service: {status}"