# test_final_state.py

import os
import csv
import pytest

def test_pipeline_report_exists():
    report_path = '/home/user/pipeline_report.csv'
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

def test_pipeline_report_content():
    report_path = '/home/user/pipeline_report.csv'
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    expected_rows = [
        ['job_id', 'step', 'exec_time_sec', 'cumulative_time'],
        ['ingest', '0', '10', '10'],
        ['clean', '1', '25', '35'],
        ['transform', '2', '40', '75'],
        ['aggregate', '3', '15', '90'],
        ['report', '4', '5', '95']
    ]

    actual_rows = []
    with open(report_path, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # Ignore empty lines if any
                actual_rows.append(row)

    assert actual_rows == expected_rows, (
        f"Content of {report_path} does not match the expected output. "
        f"Expected {expected_rows}, but got {actual_rows}."
    )