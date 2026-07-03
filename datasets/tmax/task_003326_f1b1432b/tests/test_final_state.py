# test_final_state.py

import os
import json
import pytest

def test_build_report_exists():
    """Check that the output file exists."""
    assert os.path.isfile('/home/user/build_report.json'), "The output file /home/user/build_report.json is missing."

def test_build_report_format_and_value():
    """Verify the format and the correctness of the total_metric calculated."""
    report_path = '/home/user/build_report.json'

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} is not valid JSON.")

    assert "total_metric" in report_data, f"The file {report_path} must contain the key 'total_metric'."
    actual_total = report_data["total_metric"]
    assert isinstance(actual_total, int), "The value of 'total_metric' must be an integer."

    # Calculate the expected value directly from the artifact files to ensure robustness
    expected_total = 0
    for i in range(1000):
        manifest_path = f'/home/user/artifacts/manifest_{i}.json'
        assert os.path.isfile(manifest_path), f"Input file {manifest_path} is missing."

        with open(manifest_path, 'r') as f:
            data = json.load(f)

        for j, dep in enumerate(data.get("dependencies", [])):
            size = dep.get("size_bytes", 0)
            expected_total += (size * (j + 1)) % 9973

    assert actual_total == expected_total, f"Expected total_metric to be {expected_total}, but got {actual_total}."