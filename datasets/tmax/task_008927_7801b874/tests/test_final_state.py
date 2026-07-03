# test_final_state.py

import os
import pytest

def test_files_exist():
    """Test that the required scripts and output files exist."""
    required_files = [
        "/home/user/run_analysis.sh",
        "/home/user/find_cycle.cpp",
        "/home/user/latest_deps.csv",
        "/home/user/deadlock.txt"
    ]
    for filepath in required_files:
        assert os.path.exists(filepath), f"Required file {filepath} is missing."

def test_latest_deps_csv():
    """Test that the CSV file contains the correct latest dependencies."""
    csv_path = "/home/user/latest_deps.csv"
    assert os.path.exists(csv_path), f"File missing: {csv_path}"

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Expected latest dependencies (task_id, depends_on) where depends_on is not NULL
    # 10,20
    # 20,30
    # 30,40
    # 40,50
    # 50,10
    # 60,10

    expected_pairs = {
        ("10", "20"),
        ("20", "30"),
        ("30", "40"),
        ("40", "50"),
        ("50", "10"),
        ("60", "10")
    }

    actual_pairs = set()
    for line in lines:
        parts = line.split(',')
        assert len(parts) == 2, f"Invalid CSV line format: {line}"
        actual_pairs.add((parts[0].strip(), parts[1].strip()))

    assert actual_pairs == expected_pairs, f"CSV dependencies do not match expected latest state. Got: {actual_pairs}"

def test_deadlock_txt():
    """Test that the deadlock file contains the correct sorted cycle tasks."""
    txt_path = "/home/user/deadlock.txt"
    assert os.path.exists(txt_path), f"File missing: {txt_path}"

    with open(txt_path, 'r') as f:
        content = f.read().strip()

    expected_content = "10,20,30,40,50"
    assert content == expected_content, f"Expected deadlock.txt to contain '{expected_content}', but got '{content}'."