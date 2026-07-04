# test_final_state.py
import os
import pytest

def test_rust_source_exists():
    file_path = "/home/user/analyze_backups.rs"
    assert os.path.isfile(file_path), f"Rust source file not found: {file_path}"

def test_rust_binary_exists():
    file_path = "/home/user/analyze_backups"
    assert os.path.isfile(file_path), f"Compiled Rust binary not found: {file_path}"
    assert os.access(file_path, os.X_OK), f"File is not executable: {file_path}"

def test_report_csv_content():
    file_path = "/home/user/report.csv"
    assert os.path.isfile(file_path), f"Report file not found: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = """instance_id,shortest_latency_ms,backup_size_gb
db-05,37,45
db-06,40,30
db-02,15,12"""

    assert content == expected_content, f"Content mismatch in {file_path}. Expected:\n{expected_content}\nGot:\n{content}"