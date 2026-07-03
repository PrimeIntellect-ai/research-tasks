# test_final_state.py
import os
import sys
import time
import requests
import redis
import subprocess
import pytest

def test_sanitizer_adversarial_corpus():
    sys.path.insert(0, '/home/user/app')
    try:
        import sanitizer
    except ImportError:
        pytest.fail("Failed to import sanitizer.py from /home/user/app")

    assert hasattr(sanitizer, 'validate_dataset'), "sanitizer.py is missing validate_dataset function"

    evil_dir = '/home/user/eval_corpus/evil'
    clean_dir = '/home/user/eval_corpus/clean'

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]

    evil_bypassed = []
    for f in evil_files:
        try:
            res = sanitizer.validate_dataset(f)
            if res is not False:
                evil_bypassed.append(os.path.basename(f))
        except Exception:
            pass # exceptions are acceptable if they prevent invalid data processing, but returning False is strictly preferred.

    clean_rejected = []
    for f in clean_files:
        try:
            res = sanitizer.validate_dataset(f)
            if res is not True:
                clean_rejected.append(os.path.basename(f))
        except Exception:
            clean_rejected.append(os.path.basename(f))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_msg.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_rejected)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))

def test_integration_and_services():
    # Kill any existing processes just in case
    subprocess.run(["pkill", "-f", "redis-server"], capture_output=True)
    subprocess.run(["pkill", "-f", "gunicorn"], capture_output=True)
    subprocess.run(["pkill", "-f", "nginx"], capture_output=True)

    start_script = "/home/user/app/start_services.sh"
    assert os.path.isfile(start_script), "start_services.sh is missing"

    # Start services
    subprocess.Popen([start_script], cwd="/home/user/app")
    time.sleep(3) # Wait for services to start

    r = redis.Redis(host='localhost', port=6379, db=0)
    try:
        r.ping()
    except redis.ConnectionError:
        pytest.fail("Redis is not running on port 6379")

    r.delete('dataset_queue')

    clean_file = "/home/user/eval_corpus/clean/data1.csv"
    evil_file = "/home/user/eval_corpus/evil/data1.csv"

    # Test clean upload
    try:
        with open(clean_file, 'rb') as f:
            resp = requests.post("http://localhost:8080/upload", files={'file': f}, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Nginx is not listening on port 8080 or failed to proxy to Flask")

    assert resp.status_code == 200, f"Expected HTTP 200 for clean file, got {resp.status_code}"

    queue_len = r.llen('dataset_queue')
    assert queue_len == 1, f"Expected 1 item in Redis dataset_queue, got {queue_len}"

    # Test evil upload
    with open(evil_file, 'rb') as f:
        resp = requests.post("http://localhost:8080/upload", files={'file': f}, timeout=5)

    assert resp.status_code == 400, f"Expected HTTP 400 for evil file, got {resp.status_code}"

    queue_len = r.llen('dataset_queue')
    assert queue_len == 1, f"Expected still 1 item in Redis dataset_queue, got {queue_len} (evil file bypassed queue check)"