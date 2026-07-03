# test_final_state.py
import os

def test_directory_exists():
    """Verify that the mesh_simulation directory was created."""
    assert os.path.isdir("/home/user/mesh_simulation"), "Directory /home/user/mesh_simulation does not exist."

def test_files_exist():
    """Verify that all required files exist."""
    required_files = [
        "graph.txt",
        "simulate.c",
        "Makefile",
        "results.txt"
    ]
    for filename in required_files:
        path = os.path.join("/home/user/mesh_simulation", filename)
        assert os.path.isfile(path), f"Required file {path} is missing."

def test_results_contents():
    """Verify that results.txt contains the exact expected output."""
    results_path = "/home/user/mesh_simulation/results.txt"
    assert os.path.isfile(results_path), f"{results_path} is missing."

    with open(results_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "P(0)=0.202500",
        "P(1)=0.302300",
        "P(2)=0.297400",
        "P(3)=0.197800",
        "KL=0.000055"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in results.txt, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch on line {i+1} in results.txt. Expected '{expected}', got '{actual}'."