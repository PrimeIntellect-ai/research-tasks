# test_final_state.py

import os
import pytest

def test_processed_anomalies_exists():
    """Check if processed_anomalies.csv exists."""
    file_path = "/home/user/config_tracker/processed_anomalies.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The pipeline did not produce the expected output file."

def test_processed_anomalies_contents():
    """Check if processed_anomalies.csv has the expected output."""
    file_path = "/home/user/config_tracker/processed_anomalies.csv"

    if not os.path.isfile(file_path):
        pytest.fail(f"Cannot check contents because {file_path} does not exist.")

    expected_content = """timestamp,server_id,normalized_config_key,size_bytes,rolling_avg,is_anomaly
2023-10-01T10:00:00Z,srv-01,db_port,10,10,NO
2023-10-01T10:05:00Z,srv-01,max_connections,50,30,NO
2023-10-01T10:10:00Z,srv-02,cache_size,20,20,NO
2023-10-01T10:15:00Z,srv-01,timeout_policy,60,40,NO
2023-10-01T10:20:00Z,srv-01,ssl_cert,200,103,NO
2023-10-01T10:25:00Z,srv-02,workers,20,20,NO
2023-10-01T10:30:00Z,srv-02,features,100,46,YES"""

    with open(file_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} rows (including header), but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Row {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"