# test_final_state.py
import os
import subprocess
import pytest

def test_regression_script_exists_and_executable():
    script_path = "/home/user/pipeline/regression_test.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_regression_script_execution():
    script_path = "/home/user/pipeline/regression_test.sh"
    result = subprocess.run(
        [script_path],
        cwd="/home/user/pipeline",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"regression_test.sh failed with exit code {result.returncode}. STDOUT: {result.stdout} STDERR: {result.stderr}"

def test_go_tests_pass():
    result = subprocess.run(
        ["go", "test", "./..."],
        cwd="/home/user/pipeline",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Go tests failed. STDOUT: {result.stdout} STDERR: {result.stderr}"

def test_python_tests_pass():
    result = subprocess.run(
        ["python3", "-m", "unittest", "test_aggregator.py"],
        cwd="/home/user/pipeline",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Python tests failed. STDOUT: {result.stdout} STDERR: {result.stderr}"

def test_python_aggregator_uses_decimal():
    aggregator_path = "/home/user/pipeline/aggregator.py"
    with open(aggregator_path, "r") as f:
        content = f.read()
    assert "Decimal" in content, "The Python aggregator does not seem to use the Decimal module."