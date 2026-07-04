# test_final_state.py

import os
import re
import subprocess

def test_directories_and_files_exist():
    expected_files = [
        "/home/user/scripts/monitor.sh",
        "/home/user/scripts/supervisor.sh",
        "/home/user/scripts/analyze.sh",
        "/home/user/logs/usage.csv",
        "/home/user/logs/supervisor.log",
        "/home/user/report.txt",
        "/home/user/workloads/db/init.dat",
        "/home/user/workloads/app/init.dat",
        "/home/user/workloads/db/spike.dat"
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Expected file {f} does not exist."

def test_crontab_installed():
    try:
        # Assuming the crontab is installed for the current user or 'user'
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        assert "/home/user/scripts/supervisor.sh" in result.stdout, "supervisor.sh not found in crontab."
    except subprocess.CalledProcessError:
        # Try checking for user 'user' specifically
        try:
            result = subprocess.run(["crontab", "-u", "user", "-l"], capture_output=True, text=True, check=True)
            assert "/home/user/scripts/supervisor.sh" in result.stdout, "supervisor.sh not found in user's crontab."
        except subprocess.CalledProcessError:
            assert False, "Failed to read crontab or crontab is empty."

def test_report_content():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"{report_path} not found."

    with open(report_path, "r") as f:
        content = f.read()

    assert re.search(r"db_growth_bytes:\s*5242880", content), "db_growth_bytes is not 5242880 in report.txt."
    assert re.search(r"app_growth_bytes:\s*0", content), "app_growth_bytes is not 0 in report.txt."

def test_csv_format():
    csv_path = "/home/user/logs/usage.csv"
    assert os.path.isfile(csv_path), f"{csv_path} not found."

    with open(csv_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "usage.csv is empty."

    for line in lines:
        line = line.strip()
        if line:
            assert re.match(r"^[0-9]+,(db|app),[0-9]+$", line), f"Invalid CSV format in line: '{line}'"

def test_supervisor_log_format():
    log_path = "/home/user/logs/supervisor.log"
    assert os.path.isfile(log_path), f"{log_path} not found."

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "supervisor.log is empty."

    for line in lines:
        line = line.strip()
        if line:
            assert re.match(r"^\[[0-9]+\] Restarted monitor daemon$", line), f"Invalid log format in line: '{line}'"