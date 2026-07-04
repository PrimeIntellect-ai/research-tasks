# test_final_state.py

import os
import re
import pytest

def test_ticket_resolution_log():
    log_path = "/home/user/ticket_resolution.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {log_path}, found {len(lines)}."

    scale_factor = lines[0]
    assert scale_factor == "7.5", f"Expected scale factor '7.5' on line 1, got '{scale_factor}'."

    numpy_version = lines[1]
    # Check that it looks like a version string, e.g., 1.21.6
    match = re.match(r"^1\.(\d+)(?:\.\d+)*$", numpy_version)
    assert match is not None, f"Expected a valid numpy version on line 2, got '{numpy_version}'."

    minor_version = int(match.group(1))
    assert minor_version < 23, f"Expected numpy minor version < 23 for compatibility with scipy 1.7.3, got 1.{minor_version}."

def test_final_output_csv():
    final_output_path = "/home/user/pipeline/final_output.csv"
    expected_output_path = "/home/user/pipeline/expected_output.csv"

    assert os.path.isfile(final_output_path), f"File {final_output_path} is missing. Did the script run successfully?"
    assert os.path.isfile(expected_output_path), f"File {expected_output_path} is missing."

    with open(final_output_path, "r") as f:
        final_content = f.read().strip()

    with open(expected_output_path, "r") as f:
        expected_content = f.read().strip()

    assert final_content == expected_content, f"The content of {final_output_path} does not match {expected_output_path}."

def test_virtual_environment_exists():
    venv_python_path = "/home/user/math_env/bin/python"
    assert os.path.isfile(venv_python_path) or os.path.isfile("/home/user/math_env/bin/python3"), \
        "Virtual environment Python executable not found in /home/user/math_env/bin/"

def test_requirements_txt_updated():
    req_path = "/home/user/pipeline/requirements.txt"
    assert os.path.isfile(req_path), f"File {req_path} is missing."

    with open(req_path, "r") as f:
        content = f.read().lower()

    assert "scipy==1.7.3" in content, "scipy==1.7.3 is missing or modified in requirements.txt"

    # Check that numpy is present and not 1.24.0
    assert "numpy" in content, "numpy is missing from requirements.txt"
    assert "numpy==1.24.0" not in content, "numpy==1.24.0 is still in requirements.txt, conflict not resolved."