# test_final_state.py
import os
import json
import math

def test_report_json_exists():
    assert os.path.isfile('/home/user/report.json'), "/home/user/report.json is missing"

def test_report_json_content():
    with open('/home/user/report.json', 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/report.json is not a valid JSON file"

    expected_keys = [
        "rows_remaining",
        "pipeline1_dtype",
        "pipeline2_dtype",
        "pipeline1_mse",
        "pipeline2_mse",
        "pipeline1_avg_time",
        "pipeline2_avg_time"
    ]

    for key in expected_keys:
        assert key in report, f"Key '{key}' is missing in report.json"

    assert report["rows_remaining"] == 9000, f"Expected rows_remaining to be 9000, got {report['rows_remaining']}"
    assert report["pipeline1_dtype"] == "float64", f"Expected pipeline1_dtype to be 'float64', got {report['pipeline1_dtype']}"
    assert report["pipeline2_dtype"] == "int64", f"Expected pipeline2_dtype to be 'int64', got {report['pipeline2_dtype']}"

    assert isinstance(report["pipeline1_mse"], float), "pipeline1_mse must be a float"
    assert isinstance(report["pipeline2_mse"], float), "pipeline2_mse must be a float"
    assert isinstance(report["pipeline1_avg_time"], float), "pipeline1_avg_time must be a float"
    assert isinstance(report["pipeline2_avg_time"], float), "pipeline2_avg_time must be a float"

    assert report["pipeline1_mse"] > 0, "pipeline1_mse should be greater than 0"
    assert report["pipeline2_mse"] > 0, "pipeline2_mse should be greater than 0"

    # The MSEs should be close to each other because it's essentially the same data, just different dtypes
    mse_diff = abs(report["pipeline1_mse"] - report["pipeline2_mse"])
    assert mse_diff < 1e-5, f"MSEs should be very close, but difference is {mse_diff}"

def test_benchmark_script_exists():
    assert os.path.isfile('/home/user/benchmark.py'), "/home/user/benchmark.py is missing"