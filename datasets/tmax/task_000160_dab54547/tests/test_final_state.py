# test_final_state.py
import os

def test_anomaly_report_exists_and_correct():
    """Check if the anomaly report is created and contains the correct result."""
    report_path = "/home/user/anomaly_report.txt"

    assert os.path.exists(report_path), f"Output file {report_path} does not exist. Did you save the results to the correct location?"
    assert os.path.isfile(report_path), f"{report_path} is not a regular file."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "Row: 63, Posterior Mean: 3.14"
    assert content == expected_content, f"The contents of {report_path} are incorrect.\nExpected: '{expected_content}'\nFound: '{content}'"