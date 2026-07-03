# test_final_state.py

import os
import json
import math
import pytest

REPORT_PATH = "/home/user/test_report.json"

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Expected file {REPORT_PATH} to exist."

def test_report_schema():
    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    expected_keys = {"max_abs_diff", "is_reproducible", "highest_cov_pair", "highest_cov_value"}
    assert set(report.keys()) == expected_keys, f"Report keys do not match expected schema. Got {list(report.keys())}"

def test_report_values():
    with open(REPORT_PATH, 'r') as f:
        report = json.load(f)

    # Check types
    assert isinstance(report["max_abs_diff"], float), "max_abs_diff must be a float"
    assert isinstance(report["is_reproducible"], bool), "is_reproducible must be a boolean"
    assert isinstance(report["highest_cov_pair"], list), "highest_cov_pair must be a list"
    assert isinstance(report["highest_cov_value"], float), "highest_cov_value must be a float"

    # Check values
    assert report["is_reproducible"] is False, "Expected is_reproducible to be False based on the data."
    assert report["highest_cov_pair"] == ["beta", "delta"], f"Expected highest_cov_pair to be ['beta', 'delta'], got {report['highest_cov_pair']}"

    # max_abs_diff should be > 1e-5 for it to be not reproducible
    assert report["max_abs_diff"] > 1e-5, f"Expected max_abs_diff to be > 1e-5, got {report['max_abs_diff']}"

    # highest_cov_value should be positive and roughly around 1e-8
    assert report["highest_cov_value"] > 0, f"Expected highest_cov_value to be positive, got {report['highest_cov_value']}"

    # We can also check if the values are reasonably close to the expected ones (from seed 42)
    # expected max_abs_diff ~ 0.000390141
    # expected highest_cov_value ~ 1.01831e-08
    assert math.isclose(report["max_abs_diff"], 0.000390141, rel_tol=1e-2, abs_tol=1e-5), f"max_abs_diff value {report['max_abs_diff']} is not close to expected value."
    assert math.isclose(report["highest_cov_value"], 1.01831e-08, rel_tol=1e-2, abs_tol=1e-9), f"highest_cov_value value {report['highest_cov_value']} is not close to expected value."