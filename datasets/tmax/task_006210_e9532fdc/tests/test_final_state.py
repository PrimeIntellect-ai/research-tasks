# test_final_state.py

import os
import subprocess
import pytest

def test_scripts_exist_and_executable():
    scripts = [
        "/home/user/build.sh",
        "/home/user/run_interpreter.sh",
        "/home/user/test.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_build_script_succeeds():
    build_script = "/home/user/build.sh"
    result = subprocess.run([build_script], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"build.sh failed with exit code {result.returncode}. Stderr: {result.stderr}"

def test_test_script_produces_correct_output():
    test_script = "/home/user/test.sh"
    result = subprocess.run([test_script], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"test.sh failed with exit code {result.returncode}. Stderr: {result.stderr}"

    actual_output_file = "/home/user/actual_output.txt"
    assert os.path.isfile(actual_output_file), f"Output file {actual_output_file} was not created."

    with open(actual_output_file, "r") as f:
        actual_content = f.read().strip().splitlines()

    expected_content = ["-10", "ERROR", "30", "140"]

    assert actual_content == expected_content, f"Content of {actual_output_file} does not match expected. Got: {actual_content}, Expected: {expected_content}"