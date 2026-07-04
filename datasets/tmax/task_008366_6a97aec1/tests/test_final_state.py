# test_final_state.py

import os
import subprocess
import pytest

def test_openblas_installed():
    """Verify that libopenblas-dev is installed."""
    try:
        result = subprocess.run(
            ["dpkg", "-s", "libopenblas-dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert result.returncode == 0, "libopenblas-dev is not installed."
        assert "Status: install ok installed" in result.stdout, "libopenblas-dev is not fully installed."
    except FileNotFoundError:
        pytest.fail("dpkg command not found, cannot verify libopenblas-dev installation.")

def test_source_code_exists():
    """Verify that the C source code exists."""
    assert os.path.isfile("/home/user/etl_recommend.c"), "The C source file /home/user/etl_recommend.c does not exist."

def test_executable_exists():
    """Verify that the compiled executable exists."""
    assert os.path.isfile("/home/user/etl_recommend"), "The compiled executable /home/user/etl_recommend does not exist."
    assert os.access("/home/user/etl_recommend", os.X_OK), "/home/user/etl_recommend is not executable."

def test_recommendations_output():
    """Verify that the recommendations output is correct."""
    output_file = "/home/user/recommendations.csv"
    assert os.path.isfile(output_file), f"The output file {output_file} does not exist."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1,101",
        "2,103",
        "4,104",
        "6,102"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."