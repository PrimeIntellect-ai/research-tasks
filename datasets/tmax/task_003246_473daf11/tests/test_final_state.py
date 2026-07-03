# test_final_state.py

import os
import gzip
import json
import pytest

def test_legacy_logs_deleted():
    dir_path = "/home/user/legacy_logs"
    assert not os.path.exists(dir_path), f"Directory {dir_path} should have been deleted."

def test_processed_logs_directory_exists():
    dir_path = "/home/user/processed_logs"
    assert os.path.isdir(dir_path), f"Directory {dir_path} must exist."

def test_payment_svc_archive():
    file_path = "/home/user/processed_logs/payment_svc_archive.json.gz"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with gzip.open(file_path, 'rt') as f:
        lines = [json.loads(line.strip()) for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 valid JSON lines in {file_path}, found {len(lines)}"

    assert lines[0] == {"level": "INFO", "date": "2023-01-01", "message": "Service started"}
    assert lines[1] == {"level": "ERROR", "date": "2023-01-02", "message": "Payment failed for user 123"}
    assert lines[2] == {"level": "WARN", "date": "2023-01-03", "message": "Retry attempt 1"}

def test_auth_svc_archive():
    file_path = "/home/user/processed_logs/auth_svc_archive.json.gz"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with gzip.open(file_path, 'rt') as f:
        lines = [json.loads(line.strip()) for line in f if line.strip()]

    assert len(lines) == 2, f"Expected 2 valid JSON lines in {file_path}, found {len(lines)}"

    assert lines[0] == {"level": "INFO", "date": "2023-02-01", "message": "Auth service boot"}
    assert lines[1] == {"level": "INFO", "date": "2023-02-01", "message": "User admin logged in"}

def test_inventory_svc_archive():
    file_path = "/home/user/processed_logs/inventory_svc_archive.json.gz"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with gzip.open(file_path, 'rt') as f:
        lines = [json.loads(line.strip()) for line in f if line.strip()]

    assert len(lines) == 1, f"Expected 1 valid JSON line in {file_path}, found {len(lines)}"

    assert lines[0] == {"level": "ERROR", "date": "2023-03-05", "message": "Out of stock item 999"}