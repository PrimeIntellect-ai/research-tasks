# test_final_state.py

import os
import subprocess
import json
import urllib.request
import socket
import redis
import pytest

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def test_services_running():
    assert check_port(8080), "Nginx is not listening on port 8080"
    assert check_port(5000), "Flask is not listening on port 5000"
    assert check_port(6379), "Redis is not listening on port 6379"

def test_nginx_proxy_to_flask_and_redis():
    # Connect to Redis and clear the queue first
    try:
        r = redis.Redis(host='127.0.0.1', port=6379, db=0, socket_connect_timeout=2)
        r.ping()
        r.delete('sensor_jobs')
    except Exception as e:
        pytest.fail(f"Failed to connect to Redis: {e}")

    # Make POST request through Nginx
    data = json.dumps({"filepath": "/test_path_123"}).encode('utf-8')
    req = urllib.request.Request(
        "http://127.0.0.1:8080/api/enqueue", 
        data=data, 
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status in [200, 201, 202, 204], f"Unexpected HTTP status code: {response.status}"
    except Exception as e:
        pytest.fail(f"HTTP POST to Nginx failed: {e}")

    # Check Redis for the pushed job
    try:
        job = r.lpop('sensor_jobs')
        assert job is not None, "No job found in Redis 'sensor_jobs' queue. The API did not push the payload correctly."
        assert job.decode('utf-8') == "/test_path_123", f"Unexpected job payload in Redis: {job.decode('utf-8')}"
    except Exception as e:
        pytest.fail(f"Failed to verify Redis queue: {e}")

def test_detector_binary_exists():
    assert os.path.isfile("/app/detector"), "/app/detector binary does not exist. Did you compile it?"
    assert os.access("/app/detector", os.X_OK), "/app/detector is not executable."

def test_adversarial_corpus():
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean files found in corpus"
    assert len(evil_files) > 0, "No evil files found in corpus"

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run(["/app/detector", cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        res = subprocess.run(["/app/detector", ef], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    error_msg = []
    if clean_failed:
        error_msg.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed[:5])}")
    if evil_failed:
        error_msg.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed[:5])}")

    assert not clean_failed and not evil_failed, " | ".join(error_msg)