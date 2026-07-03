# test_final_state.py

import os
import json
import subprocess
import socket

def test_bashrc_contains_env_var():
    """Test that .bashrc contains the CAPACITY_TARGET_PORT environment variable."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.exists(bashrc_path), f"{bashrc_path} does not exist"

    with open(bashrc_path, "r") as f:
        content = f.read()

    assert "CAPACITY_TARGET_PORT=8080" in content, "CAPACITY_TARGET_PORT=8080 not found in .bashrc"

def test_capacity_report_json():
    """Test that capacity_report.json exists and contains the correct data structure and values."""
    report_path = "/home/user/capacity_report.json"
    assert os.path.exists(report_path), f"{report_path} not found"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} is not valid JSON"

    assert "total_requests" in data, "Missing 'total_requests' key in report"
    assert data["total_requests"] == 20, f"total_requests must be exactly 20, got {data['total_requests']}"

    assert "avg_latency_ms" in data, "Missing 'avg_latency_ms' key in report"
    assert isinstance(data["avg_latency_ms"], (int, float)), "avg_latency_ms must be a number (float or int)"
    assert data["avg_latency_ms"] > 0, f"avg_latency_ms must be positive, got {data['avg_latency_ms']}"

    assert "peak_rss_bytes" in data, "Missing 'peak_rss_bytes' key in report"
    assert type(data["peak_rss_bytes"]) is int, "peak_rss_bytes must be an integer"
    # The app appends 1MB per request, for 20 requests it should be at least 20MB.
    # We check for > 10MB to be safe and account for base memory.
    assert data["peak_rss_bytes"] > 10 * 1024 * 1024, f"peak_rss_bytes should reflect the memory allocations (>10MB), got {data['peak_rss_bytes']}"

def test_processes_cleaned_up():
    """Test that target_app.py is no longer running."""
    try:
        # Using [t] to prevent grep from matching itself
        output = subprocess.check_output("ps aux | grep '[t]arget_app.py'", shell=True).decode().strip()
        assert not output, f"target_app.py is still running. Found processes:\n{output}"
    except subprocess.CalledProcessError:
        # grep returns 1 if no lines matched, which means the process is properly cleaned up
        pass

def test_ports_freed():
    """Test that ports 8080 and 9090 are no longer in use."""
    for port in [8080, 9090]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                # If we can bind to the port, it means it's free
                s.bind(("127.0.0.1", port))
            except OSError:
                assert False, f"Port {port} is still in use, port forwarder or target_app may still be running."