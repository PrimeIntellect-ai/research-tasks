# test_final_state.py

import os
import math

def test_rust_project_exists():
    """Test that the Rust project directory and Cargo.toml exist."""
    project_dir = "/home/user/cost_calc"
    cargo_toml = os.path.join(project_dir, "Cargo.toml")

    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} does not exist."
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found at {cargo_toml}. Did you create a Rust project?"

def test_cost_report_exists_and_content():
    """Test that the cost_report.txt file exists and contains the correct calculated total cost."""
    report_path = "/home/user/cost_report.txt"
    assert os.path.isfile(report_path), f"Cost report file {report_path} does not exist."

    # Calculate the expected value dynamically to match the truth setup
    archive_dir = "/home/user/data_archive"
    total_bytes = 0
    if os.path.isdir(archive_dir):
        for root, _, files in os.walk(archive_dir):
            for f in files:
                total_bytes += os.path.getsize(os.path.join(root, f))

    mb_size = math.ceil(total_bytes / 1048576)
    rate = 0.035
    expected_cost = mb_size * rate
    expected_content = f"Total Cost: ${expected_cost:.2f}"

    with open(report_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Incorrect content in {report_path}. "
        f"Expected '{expected_content}', but got '{actual_content}'."
    )