# test_final_state.py

import os
import json
import pytest

RAW_LOGS_PATH = "/home/user/data/raw_logs.txt"
METRICS_PATH = "/home/user/metrics.json"
OUTPUT_PATH = "/home/user/processed_logs.jsonl"

@pytest.fixture(scope="module")
def expected_data():
    assert os.path.exists(RAW_LOGS_PATH), f"Raw logs file missing: {RAW_LOGS_PATH}"

    raw_lines = 0
    seen = set()
    deduped_logs = []

    with open(RAW_LOGS_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            raw_lines += 1
            parts = line.split("|")
            assert len(parts) == 5, f"Invalid log line format: {line}"
            ts, ip, ua, status, ep = parts
            ts = int(ts)
            status = int(status)

            tup = (ts, ip, ep)
            if tup not in seen:
                seen.add(tup)
                deduped_logs.append({
                    "timestamp": ts,
                    "ip": ip,
                    "user_agent": ua,
                    "status_code": status,
                    "endpoint": ep
                })

    groups = {}
    for log in deduped_logs:
        groups.setdefault(log["ip"], []).append({
            "timestamp": log["timestamp"],
            "user_agent": log["user_agent"],
            "status_code": log["status_code"],
            "endpoint": log["endpoint"]
        })

    for ip in groups:
        groups[ip].sort(key=lambda x: x["timestamp"])

    sorted_ips = sorted(groups.keys())

    return {
        "metrics": {
            "total_raw_lines": raw_lines,
            "total_deduplicated_lines": len(deduped_logs),
            "unique_ips": len(groups)
        },
        "groups": groups,
        "sorted_ips": sorted_ips
    }

def test_metrics_file(expected_data):
    assert os.path.exists(METRICS_PATH), f"Metrics file missing: {METRICS_PATH}"

    with open(METRICS_PATH, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse JSON in {METRICS_PATH}")

    expected_metrics = expected_data["metrics"]
    for key in ["total_raw_lines", "total_deduplicated_lines", "unique_ips"]:
        assert key in metrics, f"Missing key '{key}' in {METRICS_PATH}"
        assert metrics[key] == expected_metrics[key], \
            f"Expected {key} to be {expected_metrics[key]}, got {metrics[key]}"

def test_processed_logs_file(expected_data):
    assert os.path.exists(OUTPUT_PATH), f"Processed logs file missing: {OUTPUT_PATH}"

    actual_ips = []
    actual_groups = {}

    with open(OUTPUT_PATH, "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                pytest.fail(f"Failed to parse JSON on line {line_num} in {OUTPUT_PATH}")

            assert "ip" in data, f"Missing 'ip' on line {line_num} in {OUTPUT_PATH}"
            assert "logs" in data, f"Missing 'logs' on line {line_num} in {OUTPUT_PATH}"

            ip = data["ip"]
            actual_ips.append(ip)
            actual_groups[ip] = data["logs"]

    # Check IP sorting
    assert actual_ips == expected_data["sorted_ips"], \
        "The lines in processed_logs.jsonl are not correctly sorted by IP address or have missing/extra IPs."

    # Check logs within each IP
    for ip in actual_ips:
        expected_logs = expected_data["groups"][ip]
        actual_logs = actual_groups[ip]

        assert len(actual_logs) == len(expected_logs), \
            f"Expected {len(expected_logs)} logs for IP {ip}, got {len(actual_logs)}"

        for i, (act, exp) in enumerate(zip(actual_logs, expected_logs)):
            assert act == exp, \
                f"Mismatch in log {i} for IP {ip}. Expected {exp}, got {act}"