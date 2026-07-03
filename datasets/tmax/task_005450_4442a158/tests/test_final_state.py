# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_limit_file_content():
    """Verify that limit.txt contains the correct maximum safe string length."""
    path = "/home/user/app/limit.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "15", f"Expected {path} to contain '15', but found '{content}'."

def test_regression_test_passes():
    """Verify that the regression test file exists and passes."""
    test_path = "/home/user/app/test_monitor.py"
    assert os.path.isfile(test_path), f"Regression test file {test_path} does not exist."

    cmd = [sys.executable, "-m", "unittest", test_path]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="/home/user/app")
    assert result.returncode == 0, f"Regression test failed or crashed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_monitor_no_segfault():
    """Verify that monitor_host safely handles long strings without crashing."""
    code = (
        "import sys\n"
        "sys.path.insert(0, '/home/user/app')\n"
        "import monitor\n"
        "result = monitor.monitor_host('A' * 100)\n"
        "print(result)\n"
    )
    cmd = [sys.executable, "-c", code]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="/home/user/app")

    assert result.returncode == 0, f"Calling monitor_host with a long string crashed (likely a segmentation fault).\nSTDERR:\n{result.stderr}"
    assert "200" in result.stdout.strip(), f"Expected monitor_host to return 200, got: {result.stdout.strip()}"