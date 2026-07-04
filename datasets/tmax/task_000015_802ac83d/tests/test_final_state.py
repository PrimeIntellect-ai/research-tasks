# test_final_state.py
import os
import subprocess
import pytest

def test_trigger_txt():
    trigger_file = "/home/user/app/trigger.txt"
    assert os.path.isfile(trigger_file), f"The file {trigger_file} does not exist."
    with open(trigger_file, "r") as f:
        content = f.read().strip()
    assert content == "8492", f"The file {trigger_file} does not contain the correct triggering integer. Found: {content}"

def test_processor_fixed_exists():
    fixed_executable = "/home/user/app/processor_fixed"
    assert os.path.isfile(fixed_executable), f"The file {fixed_executable} does not exist."
    assert os.access(fixed_executable, os.X_OK), f"The file {fixed_executable} is not executable."

def test_processor_fixed_execution():
    fixed_executable = "/home/user/app/processor_fixed"

    # Test with the triggering input
    try:
        result = subprocess.run(
            [fixed_executable],
            input=b"8492\n",
            capture_output=True,
            timeout=1.0,
            check=False
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"The executable {fixed_executable} timed out (deadlocked) when processing 8492.")

    assert result.returncode == 0, f"The executable {fixed_executable} failed with exit code {result.returncode}."
    output = result.stdout.decode('utf-8').strip()
    assert "Result: 8492" in output, f"The executable did not output the correct result for 8492. Output: {output}"

def test_processor_fixed_normal_execution():
    fixed_executable = "/home/user/app/processor_fixed"

    # Test with normal inputs to ensure it still works
    try:
        result = subprocess.run(
            [fixed_executable],
            input=b"10 20 30\n",
            capture_output=True,
            timeout=1.0,
            check=False
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"The executable {fixed_executable} timed out on normal inputs.")

    assert result.returncode == 0, f"The executable {fixed_executable} failed with exit code {result.returncode}."
    output = result.stdout.decode('utf-8').strip()
    assert "Result: 60" in output, f"The executable did not output the correct result for normal inputs. Output: {output}"