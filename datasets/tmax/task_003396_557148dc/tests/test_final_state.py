# test_final_state.py

import os
import json
import re
import pytest

CLEANED_LOGS_PATH = "/home/user/cleaned_logs.jsonl"
BURST_REPORT_PATH = "/home/user/burst_report.md"

def test_cleaned_logs_jsonl():
    assert os.path.isfile(CLEANED_LOGS_PATH), f"File not found: {CLEANED_LOGS_PATH}"

    with open(CLEANED_LOGS_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) > 0, f"File is empty: {CLEANED_LOGS_PATH}"

    parsed_logs = []
    for i, line in enumerate(lines):
        try:
            log_entry = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {CLEANED_LOGS_PATH} is not valid JSON.")

        assert "timestamp" in log_entry, f"Missing 'timestamp' key in line {i+1}"
        assert "job_id" in log_entry, f"Missing 'job_id' key in line {i+1}"
        assert "normalized_message" in log_entry, f"Missing 'normalized_message' key in line {i+1}"
        parsed_logs.append(log_entry)

    # Check normalization for JOB200
    job200_logs = [log for log in parsed_logs if log["job_id"] == "JOB200"]
    assert len(job200_logs) == 5, "Expected 5 logs for JOB200"
    for log in job200_logs:
        assert log["normalized_message"] == "error connection reset by peer", \
            f"Message not properly normalized for JOB200: {log['normalized_message']}"

    # Check normalization for JOB400
    job400_logs = [log for log in parsed_logs if log["job_id"] == "JOB400"]
    assert len(job400_logs) == 4, "Expected 4 logs for JOB400"
    for log in job400_logs:
        assert log["normalized_message"] == "retrying attempt", \
            f"Message not properly normalized for JOB400: {log['normalized_message']}"

def test_burst_report():
    assert os.path.isfile(BURST_REPORT_PATH), f"File not found: {BURST_REPORT_PATH}"

    with open(BURST_REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for JOB200
    assert re.search(r"JOB200.*5", content), "Report must contain JOB200 with max burst size of 5"

    # Check for JOB400
    assert re.search(r"JOB400.*4", content), "Report must contain JOB400 with max burst size of 4"

    # Check that JOB300 is absent
    assert "JOB300" not in content, "Report should not contain JOB300 as it did not have a burst"

    # Check sorting: JOB200 should appear before JOB400
    idx_200 = content.find("JOB200")
    idx_400 = content.find("JOB400")
    assert idx_200 < idx_400, "JOB200 should be listed before JOB400 in the report"