# test_final_state.py

import os
import subprocess
import pytest

def test_rust_code_compiles_and_runs():
    """Ensure the Rust project compiles and runs without panicking."""
    project_dir = "/home/user/sim_analysis"
    assert os.path.isdir(project_dir), f"Project directory {project_dir} is missing."

    # Run the Rust program to ensure it works and generates the latest solution.txt
    result = subprocess.run(
        ["cargo", "run", "--release"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Cargo run failed or panicked.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_solution_matches_expected():
    """Verify that the generated solution.txt matches the expected Ridge regression output."""
    solution_path = "/home/user/solution.txt"
    expected_path = "/home/user/expected_solution.txt"

    assert os.path.isfile(solution_path), f"Output file {solution_path} does not exist."
    assert os.path.isfile(expected_path), f"Expected solution file {expected_path} does not exist."

    with open(solution_path, "r") as f:
        solution_lines = [line.strip() for line in f if line.strip()]

    with open(expected_path, "r") as f:
        expected_lines = [line.strip() for line in f if line.strip()]

    assert len(solution_lines) == len(expected_lines), (
        f"Output line count mismatch. Expected {len(expected_lines)} lines, "
        f"got {len(solution_lines)}."
    )

    for i, (sol, exp) in enumerate(zip(solution_lines, expected_lines)):
        assert sol == exp, (
            f"Coefficient mismatch at line {i+1}:\n"
            f"Expected: {exp}\n"
            f"Got:      {sol}"
        )