# test_final_state.py

import os
import json
import time
import threading
import urllib.request
import urllib.error
import pytest

WORKSPACE_DIR = "/home/user/gateway-pr"
REVIEW_FILE = "/home/user/pr_review.json"
GATEWAY_BIN = os.path.join(WORKSPACE_DIR, "gateway")

def test_pr_review_json():
    assert os.path.isfile(REVIEW_FILE), f"Review file {REVIEW_FILE} does not exist."
    with open(REVIEW_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REVIEW_FILE} is not valid JSON.")

    expected = {
        "builds_successfully": True,
        "handles_concurrency": True,
        "benchmark_completed": True
    }

    assert data == expected, f"Content of {REVIEW_FILE} does not match expected exact structure."

def test_gateway_executable_exists():
    assert os.path.isfile(GATEWAY_BIN), f"Gateway executable {GATEWAY_BIN} was not built."
    assert os.access(GATEWAY_BIN, os.X_OK), f"Gateway executable {GATEWAY_BIN} is not executable."

def test_server_404_not_found():
    # Wait briefly in case the server is just starting or recovering from previous tests
    time.sleep(0.1)
    url = "http://127.0.0.1:8080/invalid-path"
    try:
        urllib.request.urlopen(url)
        pytest.fail("Expected HTTP 404 for unknown route, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 404, f"Expected HTTP 404 for unknown route, got {e.code}."
    except Exception as e:
        pytest.fail(f"Failed to connect to gateway: {e}")

def test_server_200_valid_route():
    time.sleep(1.2) # Ensure rate limit bucket is clear for this IP
    url = "http://127.0.0.1:8080/api/v1/users"
    try:
        with urllib.request.urlopen(url) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8')
            assert body == "Routed to user-service-backend", f"Unexpected response body: {body}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected HTTP 200 for valid route, got {e.code}.")
    except Exception as e:
        pytest.fail(f"Failed to connect to gateway: {e}")

def test_server_rate_limiting():
    # Wait for the rate limit bucket to clear completely (1 second window)
    time.sleep(1.2)

    url = "http://127.0.0.1:8080/api/v1/orders"
    results = []

    def make_request():
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                results.append(response.status)
        except urllib.error.HTTPError as e:
            results.append(e.code)
        except Exception:
            results.append(0)

    threads = [threading.Thread(target=make_request) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    counts = {}
    for r in results:
        counts[r] = counts.get(r, 0) + 1

    assert counts.get(200, 0) == 5, f"Expected exactly 5 successful requests, got {counts.get(200, 0)}. Results: {results}"
    assert counts.get(429, 0) == 5, f"Expected exactly 5 rate-limited requests (429), got {counts.get(429, 0)}. Results: {results}"