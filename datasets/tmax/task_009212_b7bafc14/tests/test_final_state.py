# test_final_state.py
import os
import pytest

def test_deadlock_report_exists_and_correct():
    report_path = "/home/user/deadlock_report.csv"

    # Check if the file exists
    assert os.path.isfile(report_path), f"Expected output file {report_path} is missing."

    # Check the contents of the file
    with open(report_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "tx_id,out_degree",
        "T11,3",
        "T2,2",
        "T3,2",
        "T6,2",
        "T1,1"
    ]

    assert lines == expected_lines, (
        f"Contents of {report_path} do not match the expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {lines}"
    )

def test_rust_project_exists():
    project_dir = "/home/user/deadlock_analyzer"
    cargo_toml = os.path.join(project_dir, "Cargo.toml")

    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} is missing."
    assert os.path.isfile(cargo_toml), f"Cargo.toml is missing in {project_dir}. Did you use Cargo to create the project?"