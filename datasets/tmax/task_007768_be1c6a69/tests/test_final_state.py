# test_final_state.py

import os
import subprocess
import pytest

def test_deploy_script_exists_and_executable():
    path = "/home/user/deploy.sh"
    assert os.path.isfile(path), f"File {path} does not exist"
    assert os.access(path, os.X_OK), f"File {path} is not executable"

def test_deploy_script_succeeds():
    path = "/home/user/deploy.sh"
    assert os.path.isfile(path), "deploy.sh is missing, cannot run it."
    result = subprocess.run([path], capture_output=True, text=True)
    assert result.returncode == 0, f"deploy.sh failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_symlink_points_to_analyzer_v2():
    path = "/home/user/bin/analyzer"
    assert os.path.islink(path), f"Symlink {path} does not exist"
    target = os.readlink(path)
    abs_target = os.path.abspath(os.path.join(os.path.dirname(path), target))
    assert abs_target == "/home/user/bin/analyzer_v2", f"Symlink {path} points to {target}, expected /home/user/bin/analyzer_v2"

def test_final_report_exists_and_correct():
    path = "/home/user/final_report.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The analyzer might not have written to REPORT_PATH correctly."
    with open(path, "r") as f:
        content = f.read()
    assert content == "Total Mem: 7168\n", f"Expected 'Total Mem: 7168\\n', but got {repr(content)}"