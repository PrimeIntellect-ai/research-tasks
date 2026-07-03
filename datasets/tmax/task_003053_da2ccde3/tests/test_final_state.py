# test_final_state.py

import os
import time
import subprocess
import pytest
import requests
import redis

def setup_module(module):
    # Ensure any existing services are stopped before starting fresh
    os.system("pkill -f uvicorn")
    os.system("pkill -f worker.py")
    os.system("pkill -f redis-server")
    time.sleep(1)

def teardown_module(module):
    # Cleanup after tests
    os.system("pkill -f uvicorn")
    os.system("pkill -f worker.py")
    os.system("pkill -f redis-server")

def test_regression_test_passes():
    """Verify that the student created the regression test and it passes."""
    test_file = '/home/user/app/test_serialization.py'
    assert os.path.exists(test_file), f"Regression test file {test_file} does not exist."

    result = subprocess.run(['pytest', test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"Regression test failed to pass:\n{result.stdout}\n{result.stderr}"

    # Check if test_roundtrip function is actually defined in the file
    with open(test_file, 'r') as f:
        content = f.read()
    assert 'def test_roundtrip' in content, "test_roundtrip function not found in test_serialization.py"

def test_performance_metric():
    """Verify that the worker can process 100 tasks in <= 3.0 seconds."""
    # Start the services
    proc = subprocess.Popen(['bash', '/home/user/app/start_services.sh'], cwd='/home/user/app')

    # Wait for services to be ready
    r = redis.Redis(host='localhost', port=6379, db=0)
    services_ready = False
    for _ in range(50):
        try:
            if r.ping():
                res = requests.get('http://localhost:8000/docs')
                if res.status_code == 200:
                    services_ready = True
                    break
        except Exception:
            pass
        time.sleep(0.1)

    assert services_ready, "Services failed to start properly."

    r.flushdb()

    # Trigger 100 tasks
    start_time = time.time()
    for _ in range(100):
        res = requests.post('http://localhost:8000/generate')
        assert res.status_code == 200, "Failed to queue task via API"

    # Wait for processing
    while True:
        processed = r.get('processed_count')
        if processed and int(processed) >= 100:
            break
        if time.time() - start_time > 10.0:
            pytest.fail("TIMEOUT: Worker took too long to process 100 tasks (exceeded 10 seconds).")
        time.sleep(0.05)

    duration = time.time() - start_time

    # Clean up
    proc.terminate()

    assert duration <= 3.0, f"Performance metric failed: processing took {duration:.2f}s, which is > 3.0s threshold."