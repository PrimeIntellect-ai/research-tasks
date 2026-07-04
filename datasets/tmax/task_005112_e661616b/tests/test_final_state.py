# test_final_state.py

import os
import time
import urllib.request
import urllib.error
import subprocess
import pytest

def test_nginx_caching_metric():
    """
    Test that Nginx caching is properly configured by measuring the time
    it takes to perform 100 sequential requests to the /analyze endpoint.
    Without caching, this would take > 20 seconds. With caching, it should
    take <= 2.0 seconds.
    """
    start = time.time()
    for i in range(100):
        try:
            req = urllib.request.Request('http://localhost:8080/analyze')
            with urllib.request.urlopen(req, timeout=2) as response:
                status = response.status
                assert status == 200, f"Request {i+1}/100 failed: Expected 200 OK, got {status}"
        except urllib.error.URLError as e:
            pytest.fail(f"Request {i+1}/100 failed: {e}. Is Nginx/Gunicorn running and correctly configured?")

    duration = time.time() - start
    assert duration <= 2.0, (
        f"Caching metric failed: 100 requests took {duration:.2f}s. "
        f"Expected <= 2.0s. Check your Nginx proxy_cache configuration."
    )

def test_verify_capacity_script():
    """
    Test that the user created the automation script at /home/user/verify_capacity.py
    and that it exits with code 0 when run.
    """
    script_path = "/home/user/verify_capacity.py"
    assert os.path.isfile(script_path), f"Task automation script {script_path} is missing."

    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0, (
            f"Script {script_path} exited with code {result.returncode}.\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Script {script_path} timed out after 10 seconds.")