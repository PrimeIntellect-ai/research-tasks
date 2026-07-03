# test_final_state.py

import os

def test_c_file_exists():
    """Test that the C program source file exists."""
    file_path = "/home/user/find_triangles.c"
    assert os.path.isfile(file_path), f"C source file {file_path} is missing. You need to write your program here."

def test_triangles_csv_exists():
    """Test that the output CSV file exists."""
    file_path = "/home/user/triangles.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

def test_triangles_csv_content():
    """Test that the output CSV file contains the correct normalized and sorted triangles."""
    file_path = "/home/user/triangles.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    expected_lines = [
        "aaron,bella,carlos",
        "aaron,elena,greg",
        "bella,felix,ivan",
        "carlos,elena,felix",
        "greg,hannah,ivan"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.split('\n') if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected exactly {len(expected_lines)} lines in {file_path}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."