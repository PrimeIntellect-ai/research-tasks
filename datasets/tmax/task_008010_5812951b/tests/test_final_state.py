# test_final_state.py

import os
import re
import shutil
import subprocess
import pytest

def test_dummy_worker_sh():
    path = "/home/user/dummy_worker.sh"
    assert os.path.isfile(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_monitor_go_and_bin():
    go_file = "/home/user/monitor.go"
    bin_file = "/home/user/monitor"
    assert os.path.isfile(go_file), f"{go_file} does not exist."
    assert os.path.isfile(bin_file), f"{bin_file} does not exist. Did you compile the Go program?"
    assert os.access(bin_file, os.X_OK), f"{bin_file} is not executable."

def test_metrics_log_format():
    log_path = "/home/user/metrics.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"{log_path} is empty."
    for line in lines:
        assert re.match(r"^\d+,\d+,\d+$", line), f"Invalid log format in {log_path}: '{line}'. Expected '<UnixTimestamp>,<PID>,<RSS_KB>'."

def test_restarts_log_format():
    log_path = "/home/user/restarts.log"
    if os.path.isfile(log_path):
        with open(log_path, "r") as f:
            lines = f.read().splitlines()
        for line in lines:
            assert re.match(r"^\d+,RESTART$", line), f"Invalid log format in {log_path}: '{line}'. Expected '<UnixTimestamp>,RESTART'."

def test_analyze_sh():
    path = "/home/user/analyze.sh"
    assert os.path.isfile(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_report_txt_format():
    path = "/home/user/report.txt"
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, f"{path} should contain exactly two lines."
    assert re.match(r"^Max RSS: \d+ KB$", lines[0]), f"Line 1 format incorrect: {lines[0]}"
    assert re.match(r"^Restarts: \d+$", lines[1]), f"Line 2 format incorrect: {lines[1]}"

def test_analyze_sh_logic():
    """
    Test analyze.sh logic by replacing the logs with mock data,
    running the script, and checking the output.
    """
    files_to_mock = ["metrics.log", "metrics.log.1", "restarts.log", "report.txt"]

    # Backup existing files
    for f in files_to_mock:
        src = f"/home/user/{f}"
        if os.path.exists(src):
            shutil.move(src, f"{src}.bak")

    try:
        # Create mock logs
        with open("/home/user/metrics.log.1", "w") as f:
            f.write("1600000000,1234,5000\n")
            f.write("1600000001,1234,16000\n")

        with open("/home/user/metrics.log", "w") as f:
            f.write("1600000002,1235,1000\n")
            f.write("1600000003,1235,8000\n")

        with open("/home/user/restarts.log", "w") as f:
            f.write("1600000001,RESTART\n")
            f.write("1600000004,RESTART\n")

        # Run analyze.sh
        result = subprocess.run(["/home/user/analyze.sh"], cwd="/home/user", capture_output=True, text=True)
        assert result.returncode == 0, f"analyze.sh failed with return code {result.returncode}\nStderr: {result.stderr}"

        # Verify report.txt
        report_path = "/home/user/report.txt"
        assert os.path.isfile(report_path), f"analyze.sh did not generate {report_path}"

        with open(report_path, "r") as f:
            lines = f.read().splitlines()

        assert len(lines) == 2, f"{report_path} should have exactly 2 lines, got {len(lines)}"
        assert lines[0] == "Max RSS: 16000 KB", f"Expected 'Max RSS: 16000 KB', got '{lines[0]}'"
        assert lines[1] == "Restarts: 2", f"Expected 'Restarts: 2', got '{lines[1]}'"

    finally:
        # Restore original files
        for f in files_to_mock:
            src = f"/home/user/{f}"
            bak = f"{src}.bak"
            if os.path.exists(src):
                os.remove(src)
            if os.path.exists(bak):
                shutil.move(bak, src)