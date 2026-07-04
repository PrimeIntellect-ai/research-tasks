# test_final_state.py
import os
import subprocess
import csv
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_script():
    script_path = "/home/user/process_logs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}. stderr: {result.stderr}"

def test_anomalies_csv():
    csv_path = "/home/user/anomalies.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} was not created."

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    expected_rows = [
        ['Minute', 'AvgTime'],
        ['2023-10-24 10:01', '700'],
        ['2023-10-24 10:03', '516']
    ]

    assert rows == expected_rows, f"Content of {csv_path} is incorrect. Expected {expected_rows}, got {rows}."

def test_anomalous_samples_log():
    log_path = "/home/user/anomalous_samples.log"
    assert os.path.isfile(log_path), f"Output file {log_path} was not created."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "2023-10-24 10:01:15,10.0.0.xxx,500,800",
        "2023-10-24 10:01:45,10.0.0.xxx,500,600",
        "2023-10-24 10:03:05,172.16.0.xxx,503,400",
        "2023-10-24 10:03:35,172.16.0.xxx,503,600",
        "2023-10-24 10:03:50,172.16.0.xxx,500,550"
    ]

    assert lines == expected_lines, f"Content of {log_path} is incorrect. Expected {expected_lines}, got {lines}."