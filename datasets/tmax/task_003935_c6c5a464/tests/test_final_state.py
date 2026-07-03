# test_final_state.py

import os
import pytest

def test_processed_nodes_file_exists():
    """Test that the processed_nodes.csv file exists."""
    file_path = "/home/user/network_etl/processed_nodes.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} was not created."

def test_processed_nodes_content():
    """Test that the processed_nodes.csv file has the correct content."""
    file_path = "/home/user/network_etl/processed_nodes.csv"

    expected_lines = [
        "NodeID,ShortestPathFrom0,Degree",
        "0,0,2",
        "1,7,3",
        "2,5,3",
        "3,8,3",
        "4,12,1"
    ]

    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip().splitlines()

    # Strip any potential trailing commas or whitespace per line just in case,
    # but the strict requirement is the exact CSV format.
    content = [line.strip() for line in content if line.strip()]

    assert content == expected_lines, (
        f"Content of {file_path} does not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(content)}"
    )