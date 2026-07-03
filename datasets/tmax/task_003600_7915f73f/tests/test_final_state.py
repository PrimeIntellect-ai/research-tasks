# test_final_state.py

import os
import pytest

def test_tracker_script_exists():
    """Test that the tracker.py script was created."""
    assert os.path.isfile("/home/user/tracker.py"), "/home/user/tracker.py does not exist."

def test_results_file_exists():
    """Test that the tracking_results.csv file was created."""
    assert os.path.isfile("/home/user/tracking_results.csv"), "/home/user/tracking_results.csv does not exist."

def test_results_content():
    """Test that the tracking_results.csv contains the correct extracted versions."""
    results_path = "/home/user/tracking_results.csv"
    assert os.path.isfile(results_path), "Results file is missing, cannot check content."

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "backup.zip,1.2.0",
        "data.zip,2.0.1",
        "latest.zip,4.5.1"
    ]

    assert sorted(lines) == sorted(expected), f"Results content does not match expected output. Expected {sorted(expected)}, got {sorted(lines)}"