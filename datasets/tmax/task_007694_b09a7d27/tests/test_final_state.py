# test_final_state.py

import os
import subprocess
import pytest

def test_requirements_txt():
    """Verify that requirements.txt exists and contains pydantic."""
    req_path = "/home/user/requirements.txt"
    assert os.path.isfile(req_path), f"{req_path} does not exist."
    with open(req_path, "r") as f:
        content = f.read().lower()
    assert "pydantic" in content, "requirements.txt does not contain 'pydantic'."

def test_calc_py_validation_error():
    """Verify that calc.py properly validates N > 5000."""
    script_path = "/home/user/calc.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    result = subprocess.run(
        ["python", script_path, "6000"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 1, "Script did not exit with code 1 for invalid input."
    assert "Validation Error" in result.stdout.strip() or "Validation Error" in result.stderr.strip(), \
        "Script did not output 'Validation Error' for invalid input."

def test_calc_py_validation_error_zero():
    """Verify that calc.py properly validates N < 1."""
    script_path = "/home/user/calc.py"

    result = subprocess.run(
        ["python", script_path, "0"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 1, "Script did not exit with code 1 for invalid input."
    assert "Validation Error" in result.stdout.strip() or "Validation Error" in result.stderr.strip(), \
        "Script did not output 'Validation Error' for invalid input."

def test_calc_py_valid_10():
    """Verify that calc.py computes correctly for N=10."""
    script_path = "/home/user/calc.py"
    output_path = "/home/user/output.txt"

    if os.path.exists(output_path):
        os.remove(output_path)

    result = subprocess.run(
        ["python", script_path, "10"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed for N=10 with error: {result.stderr}"
    assert os.path.isfile(output_path), f"{output_path} was not created."

    with open(output_path, "r") as f:
        output_val = f.read().strip()

    assert output_val == "19", f"Expected output 19 for N=10, got '{output_val}'."

def test_calc_py_valid_1000():
    """Verify that calc.py computes correctly for N=1000."""
    script_path = "/home/user/calc.py"
    output_path = "/home/user/output.txt"

    if os.path.exists(output_path):
        os.remove(output_path)

    result = subprocess.run(
        ["python", script_path, "1000"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed for N=1000 with error: {result.stderr}"
    assert os.path.isfile(output_path), f"{output_path} was not created."

    with open(output_path, "r") as f:
        output_val = f.read().strip()

    assert output_val == "178", f"Expected output 178 for N=1000, got '{output_val}'."