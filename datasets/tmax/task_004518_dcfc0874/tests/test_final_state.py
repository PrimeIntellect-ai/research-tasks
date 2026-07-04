# test_final_state.py

import os
import time
import requests
import redis
import concurrent.futures
import pytest
import subprocess

def test_throughput_result_file():
    """Verify that the student's script saved the throughput result."""
    result_path = "/home/user/throughput_result.txt"
    assert os.path.isfile(result_path), f"Expected result file {result_path} does not exist."

    with open(result_path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {result_path} is not a valid float: {content}")

def test_verify_throughput_script():
    """Verify that the student created the verify_throughput.py script."""
    script_path = "/app/verify_throughput.py"
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."

def test_system_throughput():
    """Measure the actual system throughput and assert it meets the threshold."""
    # Ensure services are running
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
    except redis.ConnectionError:
        pytest.fail("Redis is not running or accessible on localhost:6379")

    try:
        requests.get('http://127.0.0.1:8000') # Assuming some root endpoint or just checking connection
    except requests.ConnectionError:
        pass # The API might not have a root endpoint, but we'll try the enqueue endpoint in the test

    r.flushdb()

    start_time = time.time()
    def send_req(i):
        try:
            requests.post('http://127.0.0.1:8000/enqueue', json={"id": i, "payload": "test"}, timeout=5)
        except requests.RequestException as e:
            pass # Ignore request errors for now, let the count check handle failures

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as exec:
        exec.map(send_req, range(500))

    while int(r.get('processed_count') or 0) < 500:
        time.sleep(0.1)
        if time.time() - start_time > 15:
            break # Timeout

    processed = int(r.get('processed_count') or 0)
    assert processed == 500, f"Worker only processed {processed}/500 tasks within the 15s timeout. Deadlock or severe bottleneck still present."

    elapsed = time.time() - start_time
    throughput = 500 / elapsed

    threshold = 50.0
    assert throughput >= threshold, f"Throughput was {throughput:.2f} req/sec, which is below the threshold of {threshold} req/sec."