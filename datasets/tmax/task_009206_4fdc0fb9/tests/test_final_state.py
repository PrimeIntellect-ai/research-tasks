# test_final_state.py

import os
import pytest

def test_bucket_stats_csv_content():
    file_path = "/home/user/bucket_stats.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 4, "bucket_stats.csv does not contain enough rows."

    header = lines[0]
    assert header == "bucket_ts,count,bucket_avg,rolling_avg", f"Incorrect header in CSV: {header}"

    expected_rows = [
        "1698141600,3,500,500",
        "1698141660,3,400,400",
        "1698141720,2,1000,700"
    ]

    for i, expected_row in enumerate(expected_rows, start=1):
        assert lines[i] == expected_row, f"Row {i} in CSV mismatch. Expected '{expected_row}', got '{lines[i]}'"

def test_alerts_md_content():
    file_path = "/home/user/alerts.md"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_alert_1 = """## Alert for Bucket 1698141600
- Average Response Time: 500ms
- Rolling Average at bucket end: 500ms
- Request Count: 3"""

    expected_alert_2 = """## Alert for Bucket 1698141720
- Average Response Time: 1000ms
- Rolling Average at bucket end: 700ms
- Request Count: 2"""

    assert expected_alert_1 in content, "First expected alert block is missing or malformed in alerts.md."
    assert expected_alert_2 in content, "Second expected alert block is missing or malformed in alerts.md."
    assert "1698141660" not in content, "Alert for Bucket 1698141660 should not be generated (avg < 500)."