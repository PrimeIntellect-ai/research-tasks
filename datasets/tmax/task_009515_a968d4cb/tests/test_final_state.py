# test_final_state.py

import os
import json
import csv
import re
import ipaddress
import pytest

def get_expected_ips():
    auth_csv_path = "/home/user/logs/auth.csv"
    app_jsonl_path = "/home/user/logs/app.jsonl"

    # Process auth.csv
    failed_counts = {}
    if os.path.exists(auth_csv_path):
        with open(auth_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ip_str = row.get("ip_address", "")
                status = row.get("status", "")
                if status == "FAILED":
                    try:
                        # Validate IPv4
                        ipaddress.IPv4Address(ip_str)
                        failed_counts[ip_str] = failed_counts.get(ip_str, 0) + 1
                    except ipaddress.AddressValueError:
                        pass

    auth_suspects = {ip for ip, count in failed_counts.items() if count > 3}

    # Process app.jsonl
    app_error_ips = set()
    ipv4_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    if os.path.exists(app_jsonl_path):
        with open(app_jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                    if record.get("level") == "ERROR":
                        msg = record.get("msg", "")
                        for match in ipv4_pattern.findall(msg):
                            try:
                                ipaddress.IPv4Address(match)
                                app_error_ips.add(match)
                            except ipaddress.AddressValueError:
                                pass
                except json.JSONDecodeError:
                    pass

    return sorted(list(auth_suspects.intersection(app_error_ips)))

def test_flagged_ips_json():
    flagged_ips_path = "/home/user/flagged_ips.json"
    assert os.path.exists(flagged_ips_path), f"Output file {flagged_ips_path} does not exist."

    with open(flagged_ips_path, "r", encoding="utf-8") as f:
        try:
            flagged_ips = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {flagged_ips_path} does not contain valid JSON.")

    assert isinstance(flagged_ips, list), f"Expected a JSON array in {flagged_ips_path}."

    expected_ips = get_expected_ips()
    assert sorted(flagged_ips) == expected_ips, f"Flagged IPs do not match expected. Found: {flagged_ips}, Expected: {expected_ips}"

def test_pipeline_log():
    log_path = "/home/user/pipeline.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    expected_lines = [
        "[INFO] Pipeline started",
        "[INFO] Processing auth.csv",
        "[INFO] Processing app.jsonl",
        "[INFO] Pipeline finished"
    ]

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    for line in expected_lines:
        assert line in content, f"Expected log line '{line}' not found in {log_path}."