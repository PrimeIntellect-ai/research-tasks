# test_final_state.py

import os
import subprocess
import pytest

def test_mre_csv_exists_and_minimal():
    mre_path = "/home/user/ticket_4092/mre.csv"
    assert os.path.isfile(mre_path), f"{mre_path} does not exist."

    with open(mre_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, f"{mre_path} is empty."
    assert len(lines) <= 10, f"{mre_path} is not minimal (contains {len(lines)} lines, should be very small)."

def test_resolution_txt_correct():
    res_path = "/home/user/ticket_4092/resolution.txt"
    mre_path = "/home/user/ticket_4092/mre.csv"

    assert os.path.isfile(res_path), f"{res_path} does not exist."
    assert os.path.isfile(mre_path), f"Cannot verify {res_path} because {mre_path} is missing."

    with open(mre_path, "r") as f:
        mre_lines = len(f.readlines())

    with open(res_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"{res_path} must contain exactly two non-empty lines."
    assert lines[0] == "compute_statistics", f"Line 1 of {res_path} is incorrect. Expected 'compute_statistics', got '{lines[0]}'."
    assert lines[1] == str(mre_lines), f"Line 2 of {res_path} is incorrect. Expected '{mre_lines}', got '{lines[1]}'."

def test_rust_project_fixed_and_runs():
    project_dir = "/home/user/ticket_4092/sensor_stats"
    data_path = "/home/user/ticket_4092/sensor_data.csv"

    assert os.path.isdir(project_dir), f"{project_dir} does not exist."
    assert os.path.isfile(data_path), f"{data_path} does not exist."

    # Build and run the project
    try:
        result = subprocess.run(
            ["cargo", "run", "--release", "--", "../sensor_data.csv"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Cargo run timed out after 30 seconds.")

    assert result.returncode == 0, f"Cargo run failed with exit code {result.returncode}. Stderr: {result.stderr}"
    assert "Mean:" in result.stdout and "StdDev:" in result.stdout, "Output does not contain expected 'Mean:' and 'StdDev:' strings."
    assert "NaN" not in result.stdout, "Output contains 'NaN', which means the numerical instability is not fully fixed."