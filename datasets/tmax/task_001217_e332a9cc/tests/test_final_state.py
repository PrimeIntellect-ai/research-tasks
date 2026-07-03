# test_final_state.py

import os
import stat
import subprocess
import re
import pytest

def test_files_exist_and_permissions():
    assert os.path.exists("/home/user/analyzer.cpp"), "/home/user/analyzer.cpp does not exist."
    assert os.path.exists("/home/user/optimizer.sh"), "/home/user/optimizer.sh does not exist."
    assert os.path.exists("/home/user/finops.cron"), "/home/user/finops.cron does not exist."

    st = os.stat("/home/user/optimizer.sh")
    assert bool(st.st_mode & stat.S_IXUSR), "/home/user/optimizer.sh is not executable."

def test_cron_configuration():
    with open("/home/user/finops.cron", "r") as f:
        content = f.read().strip()

    # Match cron expression like "0 2 * * * /home/user/optimizer.sh" or "00 02 * * * /home/user/optimizer.sh"
    # Allow multiple spaces/tabs
    pattern = r"^0+\s+0*2\s+\*\s+\*\s+\*\s+/home/user/optimizer\.sh$"

    match = False
    for line in content.splitlines():
        line = line.strip()
        if re.match(pattern, line):
            match = True
            break

    assert match, "finops.cron does not contain the correct cron expression for 2:00 AM running /home/user/optimizer.sh."

def test_optimizer_execution_and_logic():
    metrics_path = "/home/user/metrics.csv"
    log_path = "/home/user/stopped_containers.log"
    analyzer_bin = "/home/user/analyzer"

    # Ensure metrics.csv is in place for the first test
    metrics_content = """c-web-01,45.2,1024.0
c-cache-02,1.2,30.5
c-db-03,3.0,150.0
c-worker-04,0.5,10.0
c-proxy-05,4.9,49.9
c-job-06,5.1,10.0"""
    with open(metrics_path, "w") as f:
        f.write(metrics_content)

    # Clean up previous runs
    if os.path.exists(log_path):
        os.remove(log_path)
    if os.path.exists(analyzer_bin):
        os.remove(analyzer_bin)

    # Run optimizer.sh
    result = subprocess.run(["/home/user/optimizer.sh"], capture_output=True, text=True)
    assert result.returncode == 0, f"optimizer.sh failed with exit code {result.returncode}. stderr: {result.stderr}"

    # Check log contents
    assert os.path.exists(log_path), f"{log_path} was not created."
    with open(log_path, "r") as f:
        log_content = f.read().strip().splitlines()

    expected_log = [
        "STOPPED: c-cache-02",
        "STOPPED: c-worker-04",
        "STOPPED: c-proxy-05"
    ]
    assert log_content == expected_log, f"Log contents do not match expected output. Got: {log_content}"

    # Remove metrics.csv and test error handling
    os.remove(metrics_path)
    result_missing = subprocess.run(["/home/user/optimizer.sh"], capture_output=True, text=True)
    assert result_missing.returncode == 1, f"optimizer.sh should exit with code 1 when metrics.csv is missing, got {result_missing.returncode}."

    # Restore metrics.csv
    with open(metrics_path, "w") as f:
        f.write(metrics_content)