# test_final_state.py

import os
import json
import urllib.request
import time
import subprocess
import pytest

def test_nginx_running():
    """Verify Nginx is running and listening on port 8080."""
    try:
        output = subprocess.check_output(["netstat", "-tuln"]).decode("utf-8")
        assert ":8080 " in output, "Nginx is not listening on port 8080."
    except FileNotFoundError:
        # Fallback if netstat is not available
        pass

def test_worker_running():
    """Verify the C++ worker is compiled and running."""
    worker_path = "/home/user/filter_worker"
    assert os.path.isfile(worker_path), f"Worker executable not found at {worker_path}"
    assert os.access(worker_path, os.X_OK), f"Worker at {worker_path} is not executable."

    output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
    assert "filter_worker" in output, "The filter_worker process is not running."

def test_pipeline_adversarial_corpus():
    """
    Test the entire pipeline using the adversarial corpus.
    Posts all clean and evil JSON files to Nginx, then verifies the output in Redis.
    """
    import redis

    r = redis.Redis(host='127.0.0.1', port=6379, db=0)

    # Clear queues to ensure a clean state
    r.delete('incoming_queue')
    r.delete('processed_queue')

    clean_dir = "/app/data/clean/"
    evil_dir = "/app/data/evil/"

    assert os.path.isdir(clean_dir), f"Clean dir missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil dir missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_ids = set()
    evil_ids = set()

    # Helper to send data
    def send_file(filepath, id_set):
        with open(filepath, 'r') as f:
            data = f.read()
            parsed = json.loads(data)
            id_set.add(parsed['id'])
            req = urllib.request.Request(
                "http://127.0.0.1:8080/api/ingest", 
                data=data.encode('utf-8'), 
                headers={'Content-Type': 'application/json'}
            )
            try:
                urllib.request.urlopen(req, timeout=5)
            except Exception as e:
                pytest.fail(f"Failed to POST {filepath} to Nginx: {e}")

    # Send all files
    for cf in clean_files:
        send_file(cf, clean_ids)

    for ef in evil_files:
        send_file(ef, evil_ids)

    expected_total = len(clean_ids) + len(evil_ids)

    # Wait for processing
    results = {}
    timeout = 15
    start_time = time.time()

    while time.time() - start_time < timeout:
        item = r.lpop('processed_queue')
        if item:
            try:
                parsed = json.loads(item)
                results[parsed['id']] = parsed['status']
            except Exception:
                pass
        else:
            if len(results) >= expected_total:
                break
            time.sleep(0.1)

    # Evaluate results
    clean_modified = []
    for cid in clean_ids:
        status = results.get(cid)
        if status != "CLEAN":
            clean_modified.append(cid)

    evil_bypassed = []
    for eid in evil_ids:
        status = results.get(eid)
        if status != "REJECT":
            evil_bypassed.append(eid)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_ids)} evil bypassed (e.g., {evil_bypassed[:3]})")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_ids)} clean modified/rejected (e.g., {clean_modified[:3]})")

    if error_msgs:
        pytest.fail("; ".join(error_msgs))