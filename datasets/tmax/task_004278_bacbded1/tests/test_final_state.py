# test_final_state.py

import os
import pytest

def test_workspace_exists():
    """Verify that the workspace directory was created."""
    assert os.path.isdir("/home/user/workspace"), "Fail: /home/user/workspace directory is missing."

@pytest.mark.parametrize("file_idx", range(4))
def test_log_files_copied(file_idx):
    """Verify that the log files were copied to the workspace."""
    log_file = f"/home/user/workspace/server_{file_idx}.log"
    assert os.path.isfile(log_file), f"Fail: Log file {log_file} is missing in workspace."

def test_detector_c_exists():
    """Verify that the C program source file exists."""
    assert os.path.isfile("/home/user/workspace/detector.c"), "Fail: /home/user/workspace/detector.c is missing."

def test_anomaly_txt_correct():
    """Verify that the anomaly.txt file exists and contains the correct output."""
    anomaly_file = "/home/user/anomaly.txt"
    assert os.path.isfile(anomaly_file), f"Fail: {anomaly_file} not found."

    with open(anomaly_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_content = "ANOMALY_DETECTED: 2023-10-27 14:35"
    assert content == expected_content, f"Fail: Incorrect anomaly detected. Expected '{expected_content}', Got: '{content}'"