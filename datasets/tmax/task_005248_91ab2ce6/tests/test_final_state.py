# test_final_state.py
import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/evaluator.py"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_evaluator_valid():
    cmd = ["python3", SCRIPT_PATH, "/home/user/expr_valid", "A"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}. Stderr: {result.stderr}"
    assert result.stdout.strip() == "Result: 33", f"Expected 'Result: 33', got '{result.stdout.strip()}'"

def test_evaluator_invalid_ownership():
    cmd = ["python3", SCRIPT_PATH, "/home/user/expr_invalid", "X"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 1, f"Expected exit code 1, got {result.returncode}. Stderr: {result.stderr}"
    assert result.stdout.strip() == "OwnershipError: V", f"Expected 'OwnershipError: V', got '{result.stdout.strip()}'"

def test_evaluator_cycle():
    cmd = ["python3", SCRIPT_PATH, "/home/user/expr_cycle", "P"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 2, f"Expected exit code 2, got {result.returncode}. Stderr: {result.stderr}"
    assert result.stdout.strip() == "CircularDependency", f"Expected 'CircularDependency', got '{result.stdout.strip()}'"