# test_final_state.py

import os
import urllib.request
import urllib.error
import time

def test_expect_script_exists():
    path = "/home/user/get_health.exp"
    assert os.path.isfile(path), f"Expect script not found at {path}"

def test_go_source_exists():
    path = "/home/user/monitor.go"
    assert os.path.isfile(path), f"Go source code not found at {path}"

def test_go_binary_exists_and_executable():
    path = "/home/user/monitor"
    assert os.path.isfile(path), f"Compiled Go binary not found at {path}"
    assert os.access(path, os.X_OK), f"Go binary at {path} is not executable"

def test_metrics_endpoint():
    url = "http://127.0.0.1:8080/metrics"

    # Retry a few times in case the service is slow to start
    max_retries = 3
    output = ""
    for _ in range(max_retries):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=2) as response:
                output = response.read().decode('utf-8')
                break
        except (urllib.error.URLError, ConnectionError) as e:
            time.sleep(1)
    else:
        assert False, f"Failed to connect to the metrics endpoint at {url}"

    lines = [line.strip() for line in output.split('\n') if line.strip()]

    # Check if the specific metric line exists
    expected_metric = "legacy_service_uptime_seconds 86400"
    metric_found = any(line == expected_metric for line in lines)

    assert metric_found, (
        f"Expected metric '{expected_metric}' not found in the output.\n"
        f"Actual output:\n{output}"
    )