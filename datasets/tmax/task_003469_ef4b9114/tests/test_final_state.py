# test_final_state.py
import os
import json
import re
from collections import defaultdict

def test_fuzzer_exists():
    assert os.path.isfile("/home/user/uptime_monitor/fuzzer.cpp"), "fuzzer.cpp is missing. Did you write the libFuzzer target?"

def test_uptime_report_exists():
    assert os.path.isfile("/home/user/uptime_report.json"), "/home/user/uptime_report.json is missing. Did you redirect the output?"

def test_uptime_report_content():
    log_file = "/home/user/uptime_monitor/production.log"
    assert os.path.isfile(log_file), f"{log_file} is missing."

    expected_stats = defaultdict(lambda: defaultdict(int))

    # Recompute expected stats from the log file
    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Match format: [YYYY-MM-DD] SERVICE NAME STATUS_CODE
            match = re.match(r"^\[\d{4}-\d{2}-\d{2}\]\s+(.+)\s+(\d+)$", line)
            if match:
                service_name = match.group(1).strip()
                status_code = match.group(2).strip()
                expected_stats[service_name][status_code] += 1

    # Read the generated JSON
    report_file = "/home/user/uptime_report.json"
    with open(report_file, "r") as f:
        try:
            actual_stats = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_file} does not contain valid JSON."

    # Convert expected_stats to regular dicts for comparison
    expected_stats_dict = {k: dict(v) for k, v in expected_stats.items()}

    assert actual_stats == expected_stats_dict, (
        f"The contents of {report_file} do not match the expected statistics.\n"
        f"Expected: {expected_stats_dict}\n"
        f"Actual: {actual_stats}\n"
        "Ensure you correctly handled service names with spaces and off-by-one errors in date parsing."
    )