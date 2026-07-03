# test_final_state.py

import os
import json
import subprocess
import pytest

def test_tls_certificates_exist():
    """Test that the TLS certificate and key were generated in the correct location."""
    assert os.path.exists('/home/user/cert.pem'), "/home/user/cert.pem is missing"
    assert os.path.exists('/home/user/key.pem'), "/home/user/key.pem is missing"

def test_capacity_worker_processes():
    """Test that exactly 3 capacity-worker processes are running."""
    try:
        output = subprocess.check_output(['ps', '-eo', 'args'], text=True)
        lines = output.strip().split('\n')
        # Filter out grep, pytest, and other non-worker processes that might match the string
        workers = [
            line for line in lines 
            if 'capacity-worker' in line 
            and 'grep' not in line 
            and 'pytest' not in line
            and 'monitor.go' not in line
        ]
        assert len(workers) >= 3, f"Expected at least 3 capacity-worker processes, found {len(workers)}"
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps command to check processes")

def test_go_server_listening():
    """Test that a service (Go server) is listening on port 8443."""
    try:
        output = subprocess.check_output(['ss', '-tlnp'], text=True)
        assert ':8443 ' in output, "Go server is not listening on port 8443"
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run ss command")

def test_ssh_tunnel_listening():
    """Test that the SSH tunnel is listening on port 9443."""
    try:
        output = subprocess.check_output(['ss', '-tlnp'], text=True)
        assert ':9443 ' in output, "SSH tunnel is not listening on port 9443"
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run ss command")

def test_capacity_report_json():
    """Test that the capacity report JSON file is correctly populated."""
    report_path = '/home/user/capacity_report.json'
    assert os.path.exists(report_path), f"{report_path} is missing"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} does not contain valid JSON")

    assert isinstance(data, list), "JSON root must be a list"
    assert len(data) == 3, f"Expected exactly 3 items in the report, found {len(data)}"

    for item in data:
        assert 'pid' in item, "Missing 'pid' key in report item"
        assert 'rss_kb' in item, "Missing 'rss_kb' key in report item"
        assert isinstance(item['pid'], int), "'pid' must be an integer"
        assert isinstance(item['rss_kb'], int), "'rss_kb' must be an integer"

def test_scripts_exist():
    """Test that the required script files were created."""
    assert os.path.exists('/home/user/monitor.go'), "/home/user/monitor.go is missing"
    assert os.path.exists('/home/user/fetch_metrics.sh'), "/home/user/fetch_metrics.sh is missing"