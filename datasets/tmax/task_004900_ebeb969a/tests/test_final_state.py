# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_hash():
    bad_commit_file = "/home/user/bad_commit.txt"
    assert os.path.exists(bad_commit_file), "/home/user/bad_commit.txt does not exist"

    with open(bad_commit_file, "r") as f:
        actual_hash = f.read().strip()

    repo_dir = "/home/user/sensor_project"
    cmd = ["git", "log", "--grep=Introduce calibration rounding", "--format=%H"]
    result = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True, check=True)

    # In case there are multiple matches, take the first one
    expected_hash = result.stdout.strip().split('\n')[0]

    assert expected_hash != "", "Could not find the expected bad commit in git history"
    assert actual_hash == expected_hash, f"Expected bad commit hash {expected_hash}, but got {actual_hash}"

def test_mre_script():
    mre_file = "/home/user/mre.py"
    assert os.path.exists(mre_file), "/home/user/mre.py does not exist"

    with open(mre_file, "r") as f:
        content = f.read()

    assert "apply_calibration" in content, "mre.py does not appear to use 'apply_calibration'"
    assert "100.0" in content, "mre.py does not appear to test the value 100.0"

    # Run mre.py
    env = os.environ.copy()
    # Ensure sensor_project is in PYTHONPATH so it can import src.math_utils
    env["PYTHONPATH"] = "/home/user/sensor_project"

    result = subprocess.run(["python3", mre_file], cwd="/home/user", capture_output=True, text=True, env=env)
    assert result.returncode == 0, f"mre.py failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_pipeline_tests_pass():
    repo_dir = "/home/user/sensor_project"

    # Run pytest multiple times to ensure the intermittent failure is truly fixed
    for i in range(5):
        result = subprocess.run(["pytest", "tests/test_pipeline.py"], cwd=repo_dir, capture_output=True, text=True)
        assert result.returncode == 0, f"pytest failed on run {i+1}, indicating the precision bug is not fully fixed.\nOutput: {result.stdout}\nStderr: {result.stderr}"