# test_final_state.py

import os
import stat
import re
import pytest

EXPORTER_DIR = "/home/user/exporter"
METRICS_FILE = os.path.join(EXPORTER_DIR, "metrics.prom")
SERVICE_SCRIPT = os.path.join(EXPORTER_DIR, "service.sh")
COLLECTOR_EXEC = os.path.join(EXPORTER_DIR, "collector")
QUOTA_FILE = os.path.join(EXPORTER_DIR, "quota.txt")
MOCK_ROUTE_FILE = os.path.join(EXPORTER_DIR, "mock_route.txt")

def test_directories_and_files_exist():
    """Verify that required files and directories exist."""
    assert os.path.isdir(EXPORTER_DIR), f"Directory {EXPORTER_DIR} does not exist."
    assert os.path.isfile(METRICS_FILE), f"Metrics file {METRICS_FILE} does not exist."
    assert os.path.isfile(SERVICE_SCRIPT), f"Service script {SERVICE_SCRIPT} does not exist."
    assert os.path.isfile(COLLECTOR_EXEC), f"Collector executable {COLLECTOR_EXEC} does not exist."
    assert os.path.isfile(QUOTA_FILE), f"Quota file {QUOTA_FILE} does not exist."
    assert os.path.isfile(MOCK_ROUTE_FILE), f"Mock route file {MOCK_ROUTE_FILE} does not exist."

def test_service_script_executable():
    """Verify that the service script is executable."""
    st = os.stat(SERVICE_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"{SERVICE_SCRIPT} is not executable."

def test_metrics_content():
    """Verify the contents of the generated metrics.prom file."""
    with open(METRICS_FILE, "r") as f:
        content = f.read()

    # Parse metrics
    metrics = {}
    for line in content.strip().split("\n"):
        parts = line.strip().split()
        if len(parts) == 2:
            metrics[parts[0]] = parts[1]

    assert "network_gateway_routes_total" in metrics, "network_gateway_routes_total missing in metrics.prom"
    assert metrics["network_gateway_routes_total"] == "2", f"Expected network_gateway_routes_total to be 2, got {metrics['network_gateway_routes_total']}"

    assert "disk_quota_bytes" in metrics, "disk_quota_bytes missing in metrics.prom"
    assert metrics["disk_quota_bytes"] == "53687091200", f"Expected disk_quota_bytes to be 53687091200, got {metrics['disk_quota_bytes']}"

    assert "disk_available_bytes" in metrics, "disk_available_bytes missing in metrics.prom"
    avail_bytes = metrics["disk_available_bytes"]
    assert re.match(r"^\d+$", avail_bytes), f"disk_available_bytes is not a valid integer: {avail_bytes}"
    assert int(avail_bytes) > 0, "disk_available_bytes should be greater than 0"

def test_mock_files_content():
    """Verify that the mock data files have the expected content."""
    with open(QUOTA_FILE, "r") as f:
        quota_content = f.read().strip()
    assert quota_content == "53687091200", "quota.txt does not contain the expected value."

    with open(MOCK_ROUTE_FILE, "r") as f:
        route_content = f.read().strip()

    expected_route_lines = 5  # 1 header + 4 routes
    assert len(route_content.split('\n')) >= expected_route_lines, "mock_route.txt does not contain the expected number of lines."
    assert "010011AC" in route_content, "mock_route.txt does not seem to contain the expected mock data."