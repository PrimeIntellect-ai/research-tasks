# test_final_state.py

import os
import subprocess
import urllib.request
import pytest

def test_exporter_source_and_binary_exist():
    source_path = "/home/user/exporter.c"
    binary_path = "/home/user/exporter"

    assert os.path.exists(source_path), f"C source file not found at {source_path}"
    assert os.path.exists(binary_path), f"Compiled binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"File at {binary_path} is not executable"

def test_exporter_process_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "exporter"]).decode("utf-8")
        assert len(output.strip()) > 0, "Exporter process is not running"
    except subprocess.CalledProcessError:
        pytest.fail("Exporter process is not running")

def test_ssh_tunnel_running():
    try:
        # Check for ssh port forwarding command
        output = subprocess.check_output(["pgrep", "-f", "ssh.*-L.*9090:.*8000"]).decode("utf-8")
        assert len(output.strip()) > 0, "SSH tunnel process is not running"
    except subprocess.CalledProcessError:
        pytest.fail("SSH tunnel process is not running (could not find ssh -L 9090:...:8000)")

def test_dashboard_test_log():
    log_path = "/home/user/dashboard_test.log"
    source_path = "/home/user/dashboard_data/metrics_source.txt"

    assert os.path.exists(log_path), f"Log file not found at {log_path}"
    assert os.path.exists(source_path), f"Source file not found at {source_path}"

    with open(source_path, "r") as f:
        expected_content = f.read().strip()

    with open(log_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Content of {log_path} does not match {source_path}"

def test_tunnel_responds():
    # Verify that the tunnel and exporter are actually responding correctly
    try:
        req = urllib.request.Request("http://127.0.0.1:9090/")
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            assert status == 200, f"Expected HTTP 200, got {status}"
            body = response.read().decode("utf-8").strip()

            source_path = "/home/user/dashboard_data/metrics_source.txt"
            with open(source_path, "r") as f:
                expected_content = f.read().strip()

            assert expected_content in body, "Response body does not contain expected metrics data"
    except Exception as e:
        pytest.fail(f"Failed to fetch from http://127.0.0.1:9090/ - {e}")