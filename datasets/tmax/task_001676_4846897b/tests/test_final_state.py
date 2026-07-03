# test_final_state.py
import os
import pytest

def test_report_csv_exists_and_correct():
    csv_path = "/home/user/report.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"{csv_path} is not a regular file."

    expected_lines = [
        "job_name,suite_id,size_bytes,size_rank",
        "full_cluster_backup,100,5000,1",
        "db_primary,100,2000,2",
        "db_replica,100,2000,2",
        "user_uploads,101,15000,1",
        "app_logs,101,8000,2",
        "cache_dump,102,1000,1"
    ]

    with open(csv_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Content of {csv_path} does not match expected output."

def test_go_file_exists():
    go_path = "/home/user/generate_report.go"
    assert os.path.exists(go_path), f"File {go_path} does not exist."
    assert os.path.isfile(go_path), f"{go_path} is not a regular file."