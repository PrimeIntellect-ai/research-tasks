# test_final_state.py

import os
import subprocess
import pytest

def test_process_data_executable_exists():
    """Test that the C++ source and executable exist."""
    cpp_path = "/home/user/process_data.cpp"
    exe_path = "/home/user/process_data"

    assert os.path.exists(cpp_path), f"Source file {cpp_path} does not exist."
    assert os.path.exists(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_report_content():
    """Test that the report.txt file contains the correct output."""
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_content = (
        "Data Report\n"
        "-----------\n"
        "Cleaned Metadata: T?mpSensor\n"
        "Total Records: 6\n"
        "Min: 10.50\n"
        "Max: 15.00\n"
        "Mean: 12.67"
    )

    # Normalize line endings
    content_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert content_lines == expected_lines, f"Report content mismatch.\nExpected:\n{expected_content}\nGot:\n{content}"

def test_crontab_configured():
    """Test that the crontab is configured to run the executable at 03:15 AM daily."""
    try:
        # Try to get crontab for current user (which is typically where the agent configures it)
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        crontab_output = result.stdout

        # If running as root but the agent configured it for 'user', it might be in /var/spool/cron/crontabs/user
        if not crontab_output and os.path.exists("/var/spool/cron/crontabs/user"):
            with open("/var/spool/cron/crontabs/user", "r") as f:
                crontab_output = f.read()
    except Exception:
        crontab_output = ""
        if os.path.exists("/var/spool/cron/crontabs/root"):
            with open("/var/spool/cron/crontabs/root", "r") as f:
                crontab_output += f.read()
        if os.path.exists("/var/spool/cron/crontabs/user"):
            with open("/var/spool/cron/crontabs/user", "r") as f:
                crontab_output += f.read()

    found = False
    for line in crontab_output.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 6:
            minute, hour, dom, mon, dow = parts[:5]
            command = " ".join(parts[5:])
            if minute == "15" and hour == "3" and dom == "*" and mon == "*" and dow == "*":
                if "/home/user/process_data" in command:
                    found = True
                    break

    assert found, "Crontab is not properly configured to run /home/user/process_data at 03:15 AM."