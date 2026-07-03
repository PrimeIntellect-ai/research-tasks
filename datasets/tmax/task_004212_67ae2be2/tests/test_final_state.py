# test_final_state.py

import os
import json
import math
import pytest

def test_setup_py_fixed():
    path = "/home/user/netprofiler/setup.py"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()

    assert "dpktt" not in content, f"The intentional typo 'dpktt' is still present in {path}."
    assert "dpkt" in content, f"The dependency 'dpkt' is missing from {path}."

def test_metrics_py_fixed():
    path = "/home/user/netprofiler/netprofiler/metrics.py"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()

    # The correct implementation should use absolute differences
    assert "abs(" in content, f"The file {path} does not seem to use 'abs()' to calculate absolute differences for jitter."

def test_run_analysis_exists():
    path = "/home/user/run_analysis.py"
    assert os.path.isfile(path), f"File {path} does not exist. The analysis script was not created."

def test_report_json_correct():
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"File {path} does not exist. The report was not generated."

    with open(path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    assert "total_packets" in report, "Key 'total_packets' missing from report.json"
    assert "top_src_ip" in report, "Key 'top_src_ip' missing from report.json"
    assert "mean_jitter" in report, "Key 'mean_jitter' missing from report.json"

    assert report["total_packets"] == 4, f"Expected total_packets to be 4, got {report['total_packets']}"
    assert report["top_src_ip"] == "10.0.0.1", f"Expected top_src_ip to be '10.0.0.1', got {report['top_src_ip']}"

    expected_jitter = 0.15
    actual_jitter = float(report["mean_jitter"])
    assert math.isclose(actual_jitter, expected_jitter, abs_tol=0.001), \
        f"Expected mean_jitter to be close to {expected_jitter}, got {actual_jitter}"