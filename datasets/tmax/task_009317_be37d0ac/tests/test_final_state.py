# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import time
import concurrent.futures
import pytest

def test_libfasthash_compiled():
    so_path = "/home/user/fast_process/libfasthash.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not found. Did you fix the Makefile and run make?"

def test_server_ready_file():
    ready_file = "/home/user/server_ready.txt"
    assert os.path.isfile(ready_file), f"Ready file {ready_file} was not found."
    with open(ready_file, "r") as f:
        content = f.read().strip()
    assert content == "READY", f"Expected ready file to contain exactly 'READY', but got '{content}'."

def post_request(payload_dict):
    url = "http://localhost:8080/process"
    data = json.dumps(payload_dict).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, {}
    except Exception as e:
        return None, {}

def test_server_valid_request():
    status, data = post_request({"payload": "Test"})
    assert status == 200, f"Expected HTTP 200 for valid payload, got {status}."
    # length of "Test" is 4, 'T' is 84. 4 * 100 + 84 = 484
    assert data.get("hash") == 484, f"Expected hash 484 for 'Test', got {data.get('hash')}."

def test_server_invalid_payload_format():
    status, _ = post_request({"wrong_key": "Test"})
    assert status == 400, f"Expected HTTP 400 for missing 'payload' key, got {status}."

def test_server_invalid_payload_content():
    status, _ = post_request({"payload": "Test!"})
    assert status == 400, f"Expected HTTP 400 for non-alphanumeric payload, got {status}."

def test_server_rate_limiting():
    # Wait for a fresh second window
    time.sleep(1.1)

    def make_req(_):
        return post_request({"payload": "A"})[0]

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(make_req, range(6)))

    status_200_count = results.count(200)
    status_429_count = results.count(429)

    assert status_200_count == 5, f"Expected exactly 5 successful requests, got {status_200_count}. Results: {results}"
    assert status_429_count >= 1, f"Expected at least 1 rate-limited request (HTTP 429), got {status_429_count}. Results: {results}"