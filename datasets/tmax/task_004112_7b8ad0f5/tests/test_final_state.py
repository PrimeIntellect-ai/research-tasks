# test_final_state.py

import os
import pytest

def test_clean_graph_go_exists():
    """Check that the student's Go program exists."""
    file_path = "/home/user/clean_graph.go"
    assert os.path.exists(file_path), f"Student file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_clean_backup_exists_and_correct():
    """Check that the output file exists and has the correct sorted content."""
    file_path = "/home/user/clean_backup.csv"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    expected_lines = [
        "nodeA,current_status,ACTIVE,100",
        "nodeB,current_status,INACTIVE,200",
        "nodeC,current_status,ERROR,400",
        "user1,manages,nodeA,10",
        "user4,manages,nodeA,12"
    ]

    with open(file_path, "r") as f:
        actual_content = f.read().strip()

    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {file_path} does not match the expected final state. "
        f"Expected:\n{chr(10).join(expected_lines)}\nActual:\n{chr(10).join(actual_lines)}"
    )