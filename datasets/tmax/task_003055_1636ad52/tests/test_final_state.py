# test_final_state.py

import os
import json
import subprocess
import time
import urllib.request
import pytest
import math

def test_part1_sanitizer_adversarial_corpus():
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_path), f"Sanitizer script not found at {sanitizer_path}"

    evil_corpus = "/app/corpora/evil/"
    clean_corpus = "/app/corpora/clean/"

    evil_files = [os.path.join(evil_corpus, f) for f in os.listdir(evil_corpus) if os.path.isfile(os.path.join(evil_corpus, f))]
    clean_files = [os.path.join(clean_corpus, f) for f in os.listdir(clean_corpus) if os.path.isfile(os.path.join(clean_corpus, f))]

    evil_bypassed = []
    for f in evil_files:
        result = subprocess.run(["python3", sanitizer_path, f], capture_output=True, text=True)
        # Evil files should have 0 valid lines
        if result.stdout.strip() != "":
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        result = subprocess.run(["python3", sanitizer_path, f], capture_output=True, text=True)
        with open(f, "r") as infile:
            expected = infile.read().strip()
        if result.stdout.strip() != expected:
            clean_modified.append(os.path.basename(f))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_msg, " | ".join(error_msg)


def test_part2_pipeline_worker():
    # Attempt to import redis, if missing fail test gracefully
    try:
        import redis
    except ImportError:
        pytest.fail("redis library is required but not installed.")

    r = redis.Redis(host='localhost', port=6379, db=0)

    # Check if redis is up
    try:
        r.ping()
    except redis.ConnectionError:
        pytest.fail("Redis is not running on localhost:6379")

    # Clear previous logs if any
    log_file = "/tmp/store_api_received.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    # 5 payloads as described
    payload1 = {"service_name": "model\u2160", "weights": [0.5, 0.5]}
    payload2 = {"service_name": "model\u202E", "weights": [0.5, 0.5]}
    payload3 = {"service_name": "modelI", "weights": [0.50001, 0.49999]} # Rounds to 0.5000, 0.5000
    payload4 = {"service_name": "model2", "weights": [float('nan'), 1.0]}
    payload5 = {"service_name": "model3", "weights": [0.2, 0.8]}

    # Push to redis
    r.lpush("raw_configs", json.dumps(payload1))
    r.lpush("raw_configs", json.dumps(payload2))
    r.lpush("raw_configs", json.dumps(payload3))
    r.lpush("raw_configs", json.dumps(payload4))
    r.lpush("raw_configs", json.dumps(payload5))

    # Wait for worker to process
    time.sleep(3)

    assert os.path.exists(log_file), f"Store API log not found at {log_file}. Worker might not be running or failed to send POST."

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 payloads to reach the Store API, but found {len(lines)}."

    received1 = json.loads(lines[0])
    received2 = json.loads(lines[1])

    assert received1["service_name"] == "modelI", "Payload 1 service_name not properly NFKC normalized."
    assert received2["service_name"] == "model3", "Payload 5 service_name incorrect."