# test_final_state.py

import os
import pytest

def test_edge_manager_script_exists():
    path = "/home/user/edge_manager.py"
    assert os.path.exists(path), f"The script {path} does not exist. Did you create it?"
    assert os.path.isfile(path), f"{path} is not a file."

def test_device_data_directory_exists():
    path = "/home/user/device_data"
    assert os.path.exists(path), f"The directory {path} does not exist."
    assert os.path.isdir(path), f"{path} is not a directory."

def test_edge_status_log_contents():
    path = "/home/user/edge_status.log"
    assert os.path.exists(path), f"The log file {path} was not created."

    with open(path, "r") as f:
        content = [line.strip() for line in f.readlines() if line.strip()]

    expected = [
        "STORAGE: OK",
        "CONNECTIVITY: OK",
        "DEPLOYMENT: SUCCESS"
    ]

    assert content == expected, f"Contents of {path} do not match the expected output. Got: {content}"

def test_cli_backend_log_contents():
    path = "/home/user/cli_backend.log"
    assert os.path.exists(path), f"The backend log file {path} was not created. Did the interactive script run successfully?"

    with open(path, "r") as f:
        content = [line.strip() for line in f.readlines() if line.strip()]

    expected = [
        "AUTH_SUCCESS",
        "STOPPED:legacy-sensor",
        "STARTED:vision-sensor-v2",
        "EXITED"
    ]

    assert content == expected, f"Contents of {path} do not match the expected sequence. Got: {content}"