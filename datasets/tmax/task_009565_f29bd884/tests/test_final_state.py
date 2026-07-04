# test_final_state.py

import os
import json
import pytest

def test_optimized_report_exists_and_correct():
    """Check if the optimized_report.json exists and has the correct content."""
    report_path = '/home/user/optimized_report.json'

    assert os.path.isfile(report_path), f"The report file {report_path} is missing."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    assert "top_service" in data, "Missing 'top_service' key in the report."
    assert "in_degree" in data, "Missing 'in_degree' key in the report."
    assert "avg_latency" in data, "Missing 'avg_latency' key in the report."

    assert data["top_service"] == "Auth", f"Expected top_service to be 'Auth', got '{data['top_service']}'"
    assert data["in_degree"] == 3, f"Expected in_degree to be 3, got {data['in_degree']}"
    assert float(data["avg_latency"]) == 200.0, f"Expected avg_latency to be 200.0, got {data['avg_latency']}"