# test_final_state.py

import os
import pytest

def test_crashing_ids_file():
    filepath = "/home/user/crashing_ids.txt"
    assert os.path.isfile(filepath), f"File missing: {filepath}"

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ids = {"REQ-003", "REQ-005", "REQ-008"}
    actual_ids = set(lines)

    assert actual_ids == expected_ids, f"Expected crashing IDs {expected_ids}, but got {actual_ids}"
    assert len(lines) == len(expected_ids), "There are duplicate or extra entries in crashing_ids.txt"

def test_result_file():
    filepath = "/home/user/result.txt"
    assert os.path.isfile(filepath), f"File missing: {filepath}"

    with open(filepath, "r") as f:
        content = f.read().strip()

    try:
        result_val = float(content)
    except ValueError:
        pytest.fail(f"Content of {filepath} is not a valid float: {content}")

    # The expected sum of determinants is 27.0
    assert abs(result_val - 27.0) < 1e-6, f"Expected result to be 27.0, but got {result_val}"

def test_virtual_environment_created():
    venv_dir = "/home/user/venv"
    assert os.path.isdir(venv_dir), f"Virtual environment directory missing: {venv_dir}"

    python_bin = os.path.join(venv_dir, "bin", "python")
    assert os.path.isfile(python_bin) or os.path.islink(python_bin), f"Python executable missing in venv: {python_bin}"

def test_backend_py_modified_for_error_handling():
    filepath = "/home/user/app/backend.py"
    assert os.path.isfile(filepath), f"File missing: {filepath}"

    with open(filepath, "r") as f:
        content = f.read()

    # Check if a try-except block was added
    assert "try:" in content and "except" in content, "backend.py does not appear to have try/except error handling added"