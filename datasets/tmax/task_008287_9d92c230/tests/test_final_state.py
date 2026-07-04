# test_final_state.py

import json
import os
import csv
import re
import pytest

REPORT_PATH = "/home/user/debug_report.json"
STATS_PATH = "/home/user/build_stats.csv"
DUMP_PATH = "/home/user/goroutine_dump.txt"
PCAP_PATH = "/home/user/app/traffic.pcap"

def test_debug_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Expected {REPORT_PATH} to exist."

def test_debug_report_content():
    # Derive anomalous packet size from the build stats
    anomalous_size = None
    with open(STATS_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"] == "timeout":
                anomalous_size = int(row["max_packet_size"])
                break
    assert anomalous_size is not None, "Could not derive anomalous packet size from stats."

    # Derive extracted payload from the goroutine dump
    extracted_payload = None
    with open(DUMP_PATH, "r") as f:
        content = f.read()
        match = re.search(r'last_payload\s*=\s*"([^"]+)"', content)
        if match:
            extracted_payload = match.group(1)
    assert extracted_payload is not None, "Could not derive payload from dump."

    # Derive the expected final output based on the pcap file and anomalous size
    normal_packets = 0
    with open(PCAP_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 2:
                size = int(parts[0])
                if size != anomalous_size:
                    normal_packets += 1

    expected_output = f"Success! Processed {normal_packets} normal packets."

    # Load and verify the JSON report
    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} is not valid JSON.")

    assert "anomalous_packet_size" in report, "Missing 'anomalous_packet_size' in JSON."
    assert report["anomalous_packet_size"] == anomalous_size, f"Incorrect anomalous_packet_size. Expected {anomalous_size}."

    assert "extracted_payload" in report, "Missing 'extracted_payload' in JSON."
    assert report["extracted_payload"] == extracted_payload, f"Incorrect extracted_payload. Expected '{extracted_payload}'."

    assert "fixed_output" in report, "Missing 'fixed_output' in JSON."
    assert report["fixed_output"].strip() == expected_output, f"Incorrect fixed_output. Expected '{expected_output}'."