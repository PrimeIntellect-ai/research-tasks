# test_final_state.py
import os
import pytest

def test_raw_logs_directory_empty():
    raw_logs_dir = "/home/user/raw_logs"
    assert os.path.isdir(raw_logs_dir), f"Directory {raw_logs_dir} is missing."

    raw_files = [f for f in os.listdir(raw_logs_dir) if f.endswith('.raw')]
    assert len(raw_files) == 0, f"Expected 0 .raw files in {raw_logs_dir}, found: {raw_files}"

def test_cold_storage_files():
    cold_storage_dir = "/home/user/cold_storage"
    assert os.path.isdir(cold_storage_dir), f"Directory {cold_storage_dir} is missing."

    expected_files = {
        "2023-01-10_fragment_alpha.log",
        "2023-02-14_fragment_beta.log",
        "2023-03-22_fragment_gamma.log",
        "2023-04-01_fragment_delta.log",
        "2023-05-05_fragment_epsilon.log"
    }

    actual_files = set(os.listdir(cold_storage_dir))

    for expected_file in expected_files:
        assert expected_file in actual_files, f"Expected file {expected_file} not found in {cold_storage_dir}."

def test_migration_log():
    migration_log_path = "/home/user/migration.log"
    assert os.path.isfile(migration_log_path), f"Migration log {migration_log_path} does not exist."

    expected_lines = [
        "fragment_alpha.raw -> 2023-01-10_fragment_alpha.log",
        "fragment_beta.raw -> 2023-02-14_fragment_beta.log",
        "fragment_delta.raw -> 2023-04-01_fragment_delta.log",
        "fragment_epsilon.raw -> 2023-05-05_fragment_epsilon.log",
        "fragment_gamma.raw -> 2023-03-22_fragment_gamma.log"
    ]

    with open(migration_log_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Content of {migration_log_path} is incorrect or not properly sorted. Expected:\n{expected_lines}\nGot:\n{actual_lines}"