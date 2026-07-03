# test_final_state.py
import os
import json
import re
from collections import defaultdict

def get_expected_flagged_hours():
    log_file = "/home/user/data/server_logs.txt"
    assert os.path.exists(log_file), f"Source log file {log_file} missing."

    buckets = defaultdict(lambda: {"total": 0, "errors": 0})
    with open(log_file, "r") as f:
        for line in f:
            # Match format: [YYYY-MM-DD HH:MM:SS] IP METHOD PATH HTTP_VER STATUS
            m = re.match(r"^\[(\d{4}-\d{2}-\d{2} \d{2}):\d{2}:\d{2}\].*? (\d{3})$", line.strip())
            if m:
                hour = f"{m.group(1)}:00"
                status = int(m.group(2))
                buckets[hour]["total"] += 1
                if status >= 500:
                    buckets[hour]["errors"] += 1

    expected_flagged = []
    for hour in sorted(buckets.keys()):
        total = buckets[hour]["total"]
        errors = buckets[hour]["errors"]
        rate = errors / total
        if rate > 0.05:
            expected_flagged.append({
                "hour": hour,
                "total": total,
                "errors": errors,
                "error_rate": round(rate, 4)
            })
    return expected_flagged

def test_flagged_hours_json():
    expected_flagged = get_expected_flagged_hours()
    json_file = "/home/user/flagged_hours.json"

    assert os.path.exists(json_file), f"Output file {json_file} does not exist."

    with open(json_file, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_file} is not valid JSON."

    assert isinstance(actual_data, list), f"{json_file} should contain a JSON list."
    assert len(actual_data) == len(expected_flagged), f"Expected {len(expected_flagged)} flagged hours, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_flagged)):
        assert "hour" in actual, f"Missing 'hour' key in item {i}."
        assert actual["hour"] == expected["hour"], f"Expected hour {expected['hour']}, got {actual['hour']}."

        assert "total" in actual, f"Missing 'total' key in item {i}."
        assert actual["total"] == expected["total"], f"Expected total {expected['total']}, got {actual['total']}."

        assert "errors" in actual, f"Missing 'errors' key in item {i}."
        assert actual["errors"] == expected["errors"], f"Expected errors {expected['errors']}, got {actual['errors']}."

        assert "error_rate" in actual, f"Missing 'error_rate' key in item {i}."
        assert isinstance(actual["error_rate"], float), f"'error_rate' should be a float in item {i}."
        assert abs(actual["error_rate"] - expected["error_rate"]) < 1e-5, f"Expected error_rate {expected['error_rate']}, got {actual['error_rate']}."

def test_pipeline_log():
    expected_flagged = get_expected_flagged_hours()
    log_file = "/home/user/pipeline.log"

    assert os.path.exists(log_file), f"Pipeline log file {log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read()

    expected_lines = [
        "[INFO] Stage: Extract and Bucket - Completed",
        "[INFO] Stage: Aggregate - Completed",
        "[INFO] Stage: Validation Gate - Completed"
    ]

    for line in expected_lines:
        assert line in content, f"Expected log line '{line}' not found in {log_file}."

    expected_final_line = f"[INFO] Pipeline finished. Flagged hours: {len(expected_flagged)}"
    assert expected_final_line in content, f"Expected final log line '{expected_final_line}' not found in {log_file}."