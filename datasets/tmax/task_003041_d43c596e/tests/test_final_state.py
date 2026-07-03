# test_final_state.py

import urllib.request
import urllib.error
import json
import time
import threading
import pytest

TOKEN = "blue flamingo dances brightly"
PORT = 8080
URL = f"http://127.0.0.1:{PORT}/webhook"

def test_webhook_server_unauthorized():
    """Check that the server returns 401 for missing or incorrect auth token."""
    req = urllib.request.Request(URL, method="POST")
    req.add_header("Authorization", "Bearer wrong token")
    req.add_header("Content-Type", "application/json")
    data = json.dumps({"repo": "test", "branch": "main"}).encode("utf-8")

    try:
        urllib.request.urlopen(req, data=data, timeout=2)
        pytest.fail("Server should have rejected the request with 401 Unauthorized")
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected 401 Unauthorized, got {e.code}"
    except Exception as e:
        pytest.fail(f"Unexpected error when testing unauthorized access: {e}")

def test_webhook_server_performance_and_correctness():
    """Check that the server processes requests correctly and meets the RPS threshold."""
    success_count = 0
    total_count = 200
    errors = 0

    lock = threading.Lock()

    def worker():
        nonlocal success_count, errors
        for _ in range(20):
            req = urllib.request.Request(URL, method="POST")
            req.add_header("Authorization", f"Bearer {TOKEN}")
            req.add_header("Content-Type", "application/json")
            # Mix of valid and nasty payloads to check for command injection vulnerability
            data = json.dumps({"repo": "test-repo", "branch": "main; rm -rf /"}).encode("utf-8")
            try:
                resp = urllib.request.urlopen(req, data=data, timeout=2)
                body = resp.read().decode("utf-8")
                if resp.status == 200 and "main; rm -rf /" in body and "test-repo" in body:
                    with lock:
                        success_count += 1
                else:
                    with lock:
                        errors += 1
            except Exception as e:
                with lock:
                    errors += 1

    start = time.time()
    threads = []
    for _ in range(10):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time.time() - start
    rps = total_count / duration

    assert errors == 0, f"Expected 0 errors, got {errors}. Server might be crashing or returning wrong status/body."
    assert success_count == total_count, f"Expected {total_count} successful requests, got {success_count}."

    threshold = 25.0
    assert rps >= threshold, f"Throughput too low: measured {rps:.2f} RPS, expected >= {threshold} RPS."