# test_final_state.py
import os
import json
import subprocess
import pytest
import numpy as np

def test_report_json_exists_and_valid():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"{report_path} does not exist."
    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} does not contain valid JSON.")

    assert "panic_code" in data, "report.json is missing 'panic_code'."
    assert "p95_latency" in data, "report.json is missing 'p95_latency'."

def test_panic_code_extraction():
    report_path = "/home/user/report.json"
    with open(report_path, "r") as f:
        data = json.load(f)

    assert data["panic_code"] == "0xDEADBEEF", f"Expected panic_code '0xDEADBEEF', got '{data['panic_code']}'"

def test_p95_latency_calculation():
    # Calculate true P95 from the log file
    log_path = "/app/metrics.log"
    assert os.path.isfile(log_path), f"{log_path} is missing."

    latencies = []
    with open(log_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3 and parts[2] == "200":
                latencies.append(float(parts[1]))

    assert len(latencies) > 0, "No status 200 entries found in metrics.log."

    true_p95 = float(np.percentile(latencies, 95))

    report_path = "/home/user/report.json"
    with open(report_path, "r") as f:
        data = json.load(f)

    agent_p95 = float(data["p95_latency"])
    error = abs(agent_p95 - true_p95)

    assert error <= 1.5, f"P95 latency error {error} exceeds threshold 1.5. True P95: {true_p95}, Agent P95: {agent_p95}"

def test_network_interface_sremon():
    result = subprocess.run(["ip", "link", "show", "sre-mon"], capture_output=True, text=True)
    assert result.returncode == 0, "Interface 'sre-mon' does not exist."
    assert "UP" in result.stdout or "state UP" in result.stdout or "state UNKNOWN" in result.stdout, "Interface 'sre-mon' is not brought up."

def test_network_route():
    result = subprocess.run(["ip", "route", "show"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to execute 'ip route show'."

    route_found = False
    for line in result.stdout.splitlines():
        if "10.55.0.0/24" in line and "sre-mon" in line:
            route_found = True
            break

    assert route_found, "Static route for 10.55.0.0/24 via sre-mon is missing."

def test_logrotate_config():
    conf_path = "/home/user/sre_logrotate.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "/home/user/sre_tool.log" in content, "Logrotate config does not target /home/user/sre_tool.log"
    assert "daily" in content, "Logrotate config missing 'daily' rule."
    assert "rotate 7" in content, "Logrotate config missing 'rotate 7' rule."
    assert "compress" in content, "Logrotate config missing 'compress' rule."
    assert "missingok" in content, "Logrotate config missing 'missingok' rule."