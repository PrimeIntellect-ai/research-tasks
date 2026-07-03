# test_final_state.py

import os
import json
import time
import subprocess
import re
import pytest

def test_nginx_config_fixed():
    """
    Validates that the Nginx configuration was corrected to point to the correct API port (5000).
    """
    config_path = "/app/nginx/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx config missing at {config_path}"

    with open(config_path, "r") as f:
        content = f.read()

    # The original was proxy_pass http://127.0.0.1:5001; 
    # It should be updated to point to port 5000.
    match = re.search(r"proxy_pass\s+http://(?:127\.0\.0\.1|localhost):5000/?;", content)
    assert match is not None, "Nginx config was not updated to point to the correct Flask API port (5000)."

def test_monitor_execution_and_performance():
    """
    Validates that monitor.py runs successfully, completes within the 3.0s threshold,
    and produces the correct report.json.
    """
    monitor_path = "/home/user/monitor.py"
    assert os.path.isfile(monitor_path), f"Monitor script missing at {monitor_path}"

    report_path = "/home/user/report.json"
    if os.path.exists(report_path):
        os.remove(report_path)

    # Measure execution time
    start_time = time.time()
    result = subprocess.run(["python3", monitor_path], capture_output=True, text=True)
    end_time = time.time()

    execution_time = end_time - start_time

    # Check script exit status
    assert result.returncode == 0, (
        f"FAILED: Script exited with {result.returncode}\n"
        f"stderr: {result.stderr}\n"
        f"stdout: {result.stdout}"
    )

    # Verify report.json exists and is valid
    assert os.path.exists(report_path), f"FAILED: Report file {report_path} was not created."

    try:
        with open(report_path, "r") as f:
            report = json.load(f)
    except Exception as e:
        pytest.fail(f"FAILED: Could not read or parse report.json: {e}")

    # Validate report contents
    total_requests = report.get("total_requests")
    assert total_requests == 100, f"FAILED: Expected 100 total requests, got {total_requests}"

    assert "successful_requests" in report, "FAILED: 'successful_requests' missing in report.json"
    assert "failed_requests" in report, "FAILED: 'failed_requests' missing in report.json"
    assert report["successful_requests"] + report["failed_requests"] == 100, \
        "FAILED: successful_requests + failed_requests must equal 100"

    # Metric threshold check
    assert execution_time <= 3.0, (
        f"FAILED: execution_time={execution_time:.2f}s (Threshold: <=3.0s). "
        "The script is not sufficiently optimized for concurrency."
    )