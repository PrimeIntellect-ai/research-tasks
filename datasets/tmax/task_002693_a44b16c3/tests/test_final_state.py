# test_final_state.py

import os
import subprocess
import time
import urllib.request
import pytest

def test_nginx_proxy_configuration():
    """
    Tests that the Nginx proxy is correctly configured and routes traffic
    from :8080/api/ to the mock listener on :9000.
    """
    # Run the startup script to ensure services are up
    start_script = "/home/user/app/start.sh"
    assert os.path.isfile(start_script), "Startup script missing."

    subprocess.Popen([start_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)  # Give services a moment to start

    try:
        req = urllib.request.Request("http://localhost:8080/api/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8')
            assert "ok" in body.lower(), "Expected 'ok' in response body from mock listener"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to route through Nginx proxy correctly. Error: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error while testing Nginx proxy: {e}")

def test_etl_filter_adversarial_corpus():
    """
    Tests the Rust binary against the adversarial corpus.
    Clean payloads must return exit code 0.
    Evil payloads must return a non-zero exit code.
    """
    binary_path = "/home/user/etl_filter/target/release/etl_filter"
    assert os.path.isfile(binary_path), f"Rust release binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable"

    clean_dir = "/home/user/corpus/clean"
    evil_dir = "/home/user/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean JSON files found to test."
    assert len(evil_files) > 0, "No evil JSON files found to test."

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run([binary_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        res = subprocess.run([binary_path, ef], capture_output=True)
        if res.returncode == 0:
            evil_failed.append(os.path.basename(ef))

    errors = []
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))