# test_final_state.py

import os
import subprocess
import time
import urllib.request
import urllib.error
import pytest
import signal

@pytest.fixture(scope="module")
def go_server():
    # Ensure the compiled binary exists
    binary_path = "/home/user/fs_monitor"
    assert os.path.isfile(binary_path), f"Compiled Go binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Go binary at {binary_path} is not executable"

    # Start the server
    process = subprocess.Popen([binary_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the server to start listening on port 8080
    server_up = False
    for _ in range(20):
        try:
            urllib.request.urlopen("http://localhost:8080/health", timeout=1)
            server_up = True
            break
        except Exception:
            time.sleep(0.5)

    if not server_up:
        process.terminate()
        pytest.fail("Go server did not start or bind to port 8080 within 10 seconds.")

    yield process

    # Teardown
    process.terminate()
    process.wait()

def test_files_exist_and_executable():
    expect_script = "/home/user/auto_expand.exp"
    pipeline_script = "/home/user/pipeline.sh"

    assert os.path.isfile(expect_script), f"Expect script not found at {expect_script}"
    assert os.access(expect_script, os.X_OK), f"Expect script at {expect_script} is not executable"

    assert os.path.isfile(pipeline_script), f"Pipeline script not found at {pipeline_script}"
    assert os.access(pipeline_script, os.X_OK), f"Pipeline script at {pipeline_script} is not executable"

def test_health_endpoint_empty(go_server):
    # Directories are initially empty
    req = urllib.request.Request("http://localhost:8080/health")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8').strip()
            assert body == "OK", f"Expected body 'OK', got '{body}'"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected HTTP 200 OK for empty directories, but got HTTP {e.code}")

def test_proxy_endpoint(go_server):
    req = urllib.request.Request("http://localhost:8080/backend")
    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        # Since nothing is running on 9090, it should return 502 Bad Gateway
        assert e.code in [502, 503], f"Expected 502 or 503 for proxy to dead backend, got {e.code}"
    except Exception as e:
        pytest.fail(f"Proxy endpoint request failed with unexpected error: {e}")

def test_health_endpoint_unhealthy_and_pipeline(go_server):
    pool1_dir = "/home/user/storage/pool1"
    large_file = os.path.join(pool1_dir, "largefile")

    # Create a 15MB file
    try:
        with open(large_file, "wb") as f:
            f.write(b'\0' * (15 * 1024 * 1024))

        # Test health endpoint again
        req = urllib.request.Request("http://localhost:8080/health")
        try:
            urllib.request.urlopen(req)
            pytest.fail("Expected HTTP 503 Service Unavailable, but got 200 OK")
        except urllib.error.HTTPError as e:
            assert e.code == 503, f"Expected HTTP 503, got {e.code}"
            body = e.read().decode('utf-8').strip()
            assert body == "UNHEALTHY: pool1", f"Expected body 'UNHEALTHY: pool1', got '{body}'"

        # Run pipeline script
        result = subprocess.run(["/home/user/pipeline.sh"], capture_output=True, text=True)
        assert result.returncode == 0, f"Pipeline script failed with exit code {result.returncode}. Stderr: {result.stderr}"

        # Check capacity log
        log_file = "/home/user/capacity.log"
        assert os.path.isfile(log_file), f"Log file {log_file} was not created."
        with open(log_file, "r") as f:
            log_contents = f.read()
            assert "Expanded capacity for pool1" in log_contents, f"Expected log entry not found in {log_file}. Contents: {log_contents}"

    finally:
        # Clean up
        if os.path.exists(large_file):
            os.remove(large_file)