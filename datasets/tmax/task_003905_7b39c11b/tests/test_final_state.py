# test_final_state.py

import os
import json
import pytest

def test_report_json_exists_and_correct():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist. The task requires creating this file."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not a valid JSON file.")

    assert "crash_timestamp" in data, "Missing 'crash_timestamp' key in report.json"
    expected_timestamp = "2023-10-24 10:00:07"
    assert data["crash_timestamp"] == expected_timestamp, f"Incorrect crash_timestamp. Expected '{expected_timestamp}', got '{data['crash_timestamp']}'"

    assert "recovered_token" in data, "Missing 'recovered_token' key in report.json"
    expected_token = "REC_NEW_774"
    assert data["recovered_token"] == expected_token, f"Incorrect recovered_token. Expected '{expected_token}', got '{data['recovered_token']}'"

    assert "bottleneck_substring" in data, "Missing 'bottleneck_substring' key in report.json"
    expected_substring = "ZXQPLM"
    assert data["bottleneck_substring"] == expected_substring, f"Incorrect bottleneck_substring. Expected '{expected_substring}', got '{data['bottleneck_substring']}'"