# test_final_state.py

import os
import re
import pytest

def test_extracted_logs_exist():
    logs_path = "/home/user/extracted_logs.txt"
    assert os.path.isfile(logs_path), f"Expected extracted logs file {logs_path} is missing."

    with open(logs_path, "r") as f:
        content = f.read()

    # Check if the expected latencies are present in the extracted logs
    expected_latencies = ["12.3456", "98.7654", "45.6789", "10.0001", "5.5555"]
    for val in expected_latencies:
        assert val in content, f"Expected latency value {val} not found in {logs_path}."

def test_final_report_correctness():
    report_path = "/home/user/final_report.txt"
    assert os.path.isfile(report_path), f"Expected final report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    # The expected average is 34.4691
    expected_output = "Average Latency: 34.4691"

    assert content == expected_output, f"Final report content is incorrect. Expected '{expected_output}', but got '{content}'."