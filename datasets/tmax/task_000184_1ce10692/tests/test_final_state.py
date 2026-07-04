# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/report.json"

def test_report_exists():
    """Verify that the JSON report is generated at the correct path."""
    assert os.path.exists(REPORT_PATH), f"Report file not found at {REPORT_PATH}"
    assert os.path.isfile(REPORT_PATH), f"Path {REPORT_PATH} is not a file."

def test_report_structure_and_types():
    """Verify the JSON report contains the correct keys and types."""
    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not a valid JSON file.")

    required_keys = {
        "baseline_shape",
        "optimal_n_components",
        "optimal_recall_at_10",
        "latency_raw_seconds",
        "latency_optimal_seconds"
    }

    missing_keys = required_keys - set(report.keys())
    assert not missing_keys, f"Missing required keys in report.json: {missing_keys}"

    # Check baseline shape
    assert report["baseline_shape"] == [5000, 384], \
        f"Expected baseline_shape to be [5000, 384], got {report['baseline_shape']}"

    # Check optimal components
    assert isinstance(report["optimal_n_components"], int), \
        f"optimal_n_components must be an integer, got {type(report['optimal_n_components'])}"
    assert report["optimal_n_components"] in [16, 32, 64, 128], \
        f"optimal_n_components {report['optimal_n_components']} is not in the candidate list [16, 32, 64, 128]"
    assert report["optimal_n_components"] == 64, \
        f"Expected optimal_n_components to be 64 based on the synthetic data threshold, got {report['optimal_n_components']}"

    # Check optimal recall
    assert isinstance(report["optimal_recall_at_10"], (float, int)), \
        f"optimal_recall_at_10 must be a float, got {type(report['optimal_recall_at_10'])}"
    assert 0.85 <= report["optimal_recall_at_10"] <= 1.0, \
        f"optimal_recall_at_10 should be >= 0.85 and <= 1.0, got {report['optimal_recall_at_10']}"

    recall_str = str(report["optimal_recall_at_10"])
    if "." in recall_str:
        decimals = len(recall_str.split(".")[1])
        assert decimals <= 4, \
            f"optimal_recall_at_10 should be rounded to 4 decimal places, got {report['optimal_recall_at_10']}"

    # Check latencies
    assert isinstance(report["latency_raw_seconds"], (float, int)), \
        f"latency_raw_seconds must be a float, got {type(report['latency_raw_seconds'])}"
    assert report["latency_raw_seconds"] > 0, \
        f"latency_raw_seconds must be > 0, got {report['latency_raw_seconds']}"

    assert isinstance(report["latency_optimal_seconds"], (float, int)), \
        f"latency_optimal_seconds must be a float, got {type(report['latency_optimal_seconds'])}"
    assert report["latency_optimal_seconds"] > 0, \
        f"latency_optimal_seconds must be > 0, got {report['latency_optimal_seconds']}"