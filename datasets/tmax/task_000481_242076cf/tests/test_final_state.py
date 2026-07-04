# test_final_state.py

import os
import subprocess
import time
import urllib.request
import pytest

def test_nginx_proxy_working():
    """Test that Nginx is correctly proxying requests to the Python server."""
    url = "http://localhost:8080/artifacts/bundle.zip"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            data = response.read()
            assert len(data) > 0, "Downloaded bundle.zip is empty"
    except Exception as e:
        pytest.fail(f"Failed to download from Nginx proxy at {url}: {e}")

def test_curator_binary_exists_and_executable():
    """Test that the compiled C++ binary exists and is executable."""
    curator_path = "/home/user/curator"
    assert os.path.isfile(curator_path), f"Compiled binary {curator_path} does not exist."
    assert os.access(curator_path, os.X_OK), f"Compiled binary {curator_path} is not executable."

def test_curator_execution_time_metric():
    """
    Test that the C++ program processes the large WAL file efficiently.
    Metric: Execution time <= 0.5 seconds.
    """
    curator_path = "/home/user/curator"
    wal_path = "/app/large_journal.wal"

    assert os.path.isfile(wal_path), f"Benchmark file {wal_path} is missing."

    start_time = time.perf_counter()
    result = subprocess.run([curator_path, wal_path], capture_output=True, text=True)
    end_time = time.perf_counter()

    assert result.returncode == 0, f"Curator execution failed with return code {result.returncode}.\nStderr: {result.stderr}"

    execution_time = end_time - start_time
    threshold = 0.5

    assert execution_time <= threshold, (
        f"Metric failed: Execution time was {execution_time:.4f} seconds, "
        f"which exceeds the threshold of {threshold} seconds."
    )

    # Basic sanity check that it produced some output
    assert len(result.stdout.strip()) > 0, "Curator produced no output. It should print valid paths."