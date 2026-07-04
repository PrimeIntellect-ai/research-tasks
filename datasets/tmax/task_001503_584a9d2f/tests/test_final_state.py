# test_final_state.py

import os
import subprocess
import pytest

def test_orchestrate_script_exists_and_executable():
    script_path = "/home/user/polybuild/orchestrate.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_diff_report_exists_and_correct():
    report_path = "/home/user/polybuild/diff_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected = "T001,5\nT002,-5\nT003,0"

    assert content == expected, f"Content of {report_path} is incorrect.\nExpected:\n{expected}\nActual:\n{content}"

def test_build_server_not_running():
    # Check if build_server.py is running
    try:
        output = subprocess.check_output(["pgrep", "-f", "build_server.py"], text=True)
        # If output is not empty, it means the process is still running
        assert not output.strip(), "build_server.py is still running. It was not cleanly killed."
    except subprocess.CalledProcessError:
        # pgrep returns non-zero exit code if no processes are matched, which is the expected behavior here
        pass