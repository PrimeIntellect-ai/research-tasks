# test_final_state.py

import os
import time
import subprocess
import urllib.request
import urllib.error
import pytest

def test_compiled_binary_exists():
    assert os.path.isfile("/home/user/process_docs"), "Compiled binary /home/user/process_docs is missing. Did you compile your Go code?"
    assert os.access("/home/user/process_docs", os.X_OK), "/home/user/process_docs is not executable."

def test_tar_slip_prevention():
    # Clean up any previous extraction
    if os.path.exists("/tmp/evil.txt"):
        os.remove("/tmp/evil.txt")

    # Run the agent's binary on the upload tarball
    result = subprocess.run(["/home/user/process_docs", "/app/data/docs_upload.tar"], capture_output=True, text=True)
    assert result.returncode == 0, f"process_docs failed on docs_upload.tar:\n{result.stderr}"

    # Check if the evil file was extracted outside the target directory
    assert not os.path.exists("/tmp/evil.txt"), "Tar slip vulnerability not fixed: /tmp/evil.txt was extracted outside the target directory."

def test_api_and_wal_parsing():
    # The agent's binary should have populated Redis with WAL data from docs_upload.tar
    # We test the full flow: Nginx -> Flask -> Redis
    url = "http://127.0.0.1:8080/api/doc/101"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            data = response.read().decode('utf-8').strip()

            assert status == 200, f"Expected HTTP 200, got {status}"
            assert data != "", "Expected a timestamp from the API, but got an empty response."
            assert data != "null", "Document 101 not found in Redis. WAL parsing or Redis insertion failed."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx API at {url}. Is Nginx configured correctly and running? Error: {e}")

def test_performance_speedup():
    # Run reference binary
    start_ref = time.time()
    ref_result = subprocess.run(["/app/bin/process_docs_ref", "/app/data/large_docs.tar"], capture_output=True)
    end_ref = time.time()
    assert ref_result.returncode == 0, "Reference binary failed to run."
    time_ref = end_ref - start_ref

    # Run agent binary
    start_agent = time.time()
    agent_result = subprocess.run(["/home/user/process_docs", "/app/data/large_docs.tar"], capture_output=True)
    end_agent = time.time()
    assert agent_result.returncode == 0, f"Agent binary failed on large_docs.tar:\n{agent_result.stderr.decode('utf-8', errors='ignore')}"
    time_agent = end_agent - start_agent

    # Calculate speedup
    speedup = time_ref / time_agent

    assert speedup >= 3.0, (
        f"Performance metric failed: Target speedup >= 3.0, but achieved {speedup:.2f}x. "
        f"(Ref time: {time_ref:.2f}s, Agent time: {time_agent:.2f}s). "
        "Ensure your Go code uses goroutines to process files concurrently."
    )