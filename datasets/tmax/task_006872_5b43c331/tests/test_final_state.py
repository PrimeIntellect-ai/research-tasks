# test_final_state.py

import os
import json
import glob
import pytest

PIPELINE_DIR = "/home/user/log_pipeline"
DATA_DIR = os.path.join(PIPELINE_DIR, "data")
OUTPUT_JSON = os.path.join(PIPELINE_DIR, "output.json")
REPORT_JSON = "/home/user/report.json"
ANOMALOUS_IP = "10.0.42.17"

def get_true_counts():
    counts = {}
    log_files = glob.glob(os.path.join(DATA_DIR, "*.log"))
    for filename in log_files:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(filename, "r", encoding="utf-16") as f:
                lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if data.get("status", 200) >= 500:
                    ip = data.get("ip")
                    if ip:
                        counts[ip] = counts.get(ip, 0) + 1
            except Exception:
                pass
    return counts

def test_report_json_exists_and_valid():
    assert os.path.isfile(REPORT_JSON), f"Report file {REPORT_JSON} is missing."
    with open(REPORT_JSON, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_JSON} is not valid JSON.")

    assert "anomalous_ip" in report_data, f"'anomalous_ip' missing in {REPORT_JSON}"
    assert "anomalous_error_count" in report_data, f"'anomalous_error_count' missing in {REPORT_JSON}"

    assert report_data["anomalous_ip"] == ANOMALOUS_IP, \
        f"Expected anomalous IP {ANOMALOUS_IP}, got {report_data['anomalous_ip']}."

def test_output_json_exists_and_valid():
    assert os.path.isfile(OUTPUT_JSON), f"Output file {OUTPUT_JSON} is missing."
    with open(OUTPUT_JSON, 'r') as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{OUTPUT_JSON} is not valid JSON.")

    assert isinstance(output_data, dict), f"{OUTPUT_JSON} should be a JSON object (dictionary)."

def test_error_counts_match_truth():
    true_counts = get_true_counts()

    with open(REPORT_JSON, 'r') as f:
        report_data = json.load(f)

    with open(OUTPUT_JSON, 'r') as f:
        output_data = json.load(f)

    # Check anomalous count in report
    expected_anomalous_count = true_counts.get(ANOMALOUS_IP, 0)
    assert report_data["anomalous_error_count"] == expected_anomalous_count, \
        f"Anomalous error count in report ({report_data['anomalous_error_count']}) does not match true count ({expected_anomalous_count})."

    # Check all counts in output.json
    for ip, count in true_counts.items():
        assert ip in output_data, f"IP {ip} is missing from {OUTPUT_JSON}."
        assert output_data[ip] == count, \
            f"Count for IP {ip} in {OUTPUT_JSON} is {output_data[ip]}, but true count is {count}."

    # Check that there are no extra IPs in output.json
    for ip in output_data.keys():
        assert ip in true_counts, f"IP {ip} found in {OUTPUT_JSON} but has no >= 500 errors in data."