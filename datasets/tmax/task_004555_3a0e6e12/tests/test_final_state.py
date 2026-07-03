# test_final_state.py
import os
import re
import pytest

def test_hostfile_exists_and_correct():
    """Verify that the hostfile exists and defines 4 workers with 8 slots each."""
    hostfile_path = "/home/user/hostfile"
    assert os.path.isfile(hostfile_path), f"Hostfile {hostfile_path} is missing."

    with open(hostfile_path, "r") as f:
        content = f.read()

    for i in range(4):
        worker = f"worker-{i}"
        # Match typical MPI hostfile formats like "worker-0 slots=8" or "worker-0 cpu=8"
        # Also tolerate spaces like "worker-0 slots=8" or "worker-0 slots 8"
        pattern = rf"{worker}\b.*(?:slots|cpu)s?\s*=?\s*8\b"
        assert re.search(pattern, content, re.IGNORECASE), (
            f"Could not find valid configuration for {worker} with 8 slots in {hostfile_path}. "
            f"Ensure it follows the format '{worker} slots=8'."
        )

def test_analyze_script_exists_and_executable():
    """Verify that analyze.sh exists and is executable."""
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_max_degree_output():
    """Verify the output of the graph analysis."""
    output_path = "/home/user/max_degree.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected = "Node ID: 4, Degree: 7"
    assert content == expected, (
        f"Incorrect output in {output_path}.\n"
        f"Expected: '{expected}'\n"
        f"Got: '{content}'"
    )