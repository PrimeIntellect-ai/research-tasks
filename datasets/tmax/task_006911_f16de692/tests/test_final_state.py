# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    """Check that the bash script exists and is executable."""
    script_path = "/home/user/resolve_env.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_startup_order_output():
    """Verify the topological sort output in startup_order.txt."""
    output_path = "/home/user/startup_order.txt"
    assert os.path.exists(output_path), f"The output file {output_path} does not exist."

    expected_lines = [
        "cache",
        "db",
        "auth",
        "backend",
        "frontend",
        "metrics"
    ]

    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {output_path} do not match the expected topological sort order.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {actual_lines}"
    )

def test_port_assignments_output():
    """Verify the port allocation output in port_assignments.txt."""
    output_path = "/home/user/port_assignments.txt"
    assert os.path.exists(output_path), f"The output file {output_path} does not exist."

    expected_lines = [
        "cache: 6379",
        "db: 5432",
        "auth: 5000",
        "backend: 5001",
        "frontend: 80",
        "metrics: 5002"
    ]

    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {output_path} do not match the expected port assignments.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {actual_lines}"
    )