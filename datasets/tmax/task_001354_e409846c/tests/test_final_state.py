# test_final_state.py

import os
import json
import time
import urllib.request
import urllib.error
import concurrent.futures
import pytest

APP_DIR = "/home/user/app"
CLEAN_DIR = os.path.join(APP_DIR, "corpora", "clean")
EVIL_DIR = os.path.join(APP_DIR, "corpora", "evil")
PROXY_URL = "http://127.0.0.1:8080/"

def send_request(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    req = urllib.request.Request(PROXY_URL, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return 0

def test_evil_corpus_rejected():
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.json')]
    bypassed = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        status = send_request(filepath)
        if status != 403:
            bypassed.append((filename, status))
        time.sleep(0.25)  # Avoid rate limit

    if bypassed:
        offending = ", ".join([f"{f} (status {s})" for f, s in bypassed])
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {offending}")

def test_clean_corpus_accepted():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.json')]
    modified = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        status = send_request(filepath)
        if status != 200:
            modified.append((filename, status))
        time.sleep(0.25)  # Avoid rate limit

    if modified:
        offending = ", ".join([f"{f} (status {s})" for f, s in modified])
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (failed to return 200): {offending}")

def test_rate_limiting():
    # To test rate limiting, we blast 20 concurrent requests.
    # We can use a clean payload so it would normally return 200.
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.json')]
    if not clean_files:
        pytest.skip("No clean files available for rate limit test")

    filepath = os.path.join(CLEAN_DIR, clean_files[0])

    def worker(_):
        return send_request(filepath)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(worker, range(20)))

    count_429 = results.count(429)
    count_200 = results.count(200)

    assert count_429 == 15, f"Expected 15 requests to return 429, but got {count_429}. Results: {results}"
    assert count_200 == 5, f"Expected 5 requests to succeed, but got {count_200}. Results: {results}"