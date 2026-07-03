# test_final_state.py
import os
import pytest

def test_anomaly_report_exists():
    """Check if the anomaly report HTML file was generated."""
    path = "/home/user/anomaly_report.html"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

def test_anomaly_report_content():
    """Check if the anomaly report contains the correct anomalies in chronological order."""
    path = "/home/user/anomaly_report.html"
    if not os.path.isfile(path):
        pytest.fail(f"File {path} does not exist.")

    with open(path, "r") as f:
        content = f.read()

    # Expected anomaly strings based on the template and data
    expected_s2 = "2023-10-01T10:10:00Z - S2: -10.0"
    expected_s1 = "2023-10-01T10:20:00Z - S1: 45.0"

    # Check if both are present
    assert expected_s2 in content, f"Anomaly for S2 ({expected_s2}) is missing from the report."
    assert expected_s1 in content, f"Anomaly for S1 ({expected_s1}) is missing from the report."

    # Check chronological order
    idx_s2 = content.find(expected_s2)
    idx_s1 = content.find(expected_s1)

    assert idx_s2 < idx_s1, "Anomalies are not sorted chronologically (S2 at 10:10 should appear before S1 at 10:20)."