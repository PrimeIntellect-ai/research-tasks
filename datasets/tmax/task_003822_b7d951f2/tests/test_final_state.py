# test_final_state.py

import os
import pytest

CSV_PATH = "/home/user/shortest_path.csv"
SCRIPT_PATH = "/home/user/find_path.py"

def test_script_exists():
    """Verify that the user created the Python script."""
    assert os.path.isfile(SCRIPT_PATH), f"Expected script {SCRIPT_PATH} does not exist."

def test_shortest_path_csv():
    """Verify the contents of the shortest_path.csv file."""
    assert os.path.isfile(CSV_PATH), f"Expected output file {CSV_PATH} does not exist."

    with open(CSV_PATH, "r") as f:
        content = f.read().strip().splitlines()

    expected_content = [
        "node,cumulative_latency",
        "START,0",
        "N1,2",
        "N2,3",
        "END,6"
    ]

    # Strip whitespace from each line to be flexible with CRLF/LF or trailing commas/spaces
    content = [line.strip() for line in content if line.strip()]
    expected_content = [line.strip() for line in expected_content]

    assert content == expected_content, (
        f"Contents of {CSV_PATH} do not match the expected shortest path.\n"
        f"Expected: {expected_content}\n"
        f"Got: {content}"
    )