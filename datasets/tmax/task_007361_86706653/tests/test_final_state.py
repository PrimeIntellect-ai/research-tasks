# test_final_state.py
import os

def test_monitor_files_exist():
    assert os.path.isfile("/home/user/monitor.c"), "/home/user/monitor.c is missing"
    assert os.path.isfile("/home/user/monitor"), "/home/user/monitor executable is missing"
    assert os.access("/home/user/monitor", os.X_OK), "/home/user/monitor is not executable"

def test_bad_logs_csv_contents():
    csv_path = "/home/user/bad_logs.csv"
    assert os.path.isfile(csv_path), f"{csv_path} was not created"

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "3,ERROR",
        "6,ERROR",
        "9,ERROR"
    ]

    assert lines == expected_lines, f"Contents of {csv_path} do not match the expected output. Got: {lines}"