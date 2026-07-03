# test_final_state.py

import os
import pytest

def test_output_file_exists():
    """Test that the output CSV file exists."""
    output_path = '/home/user/output/distances.csv'
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

def test_output_file_content():
    """Test that the output CSV file has the exact expected content."""
    output_path = '/home/user/output/distances.csv'

    expected_content = (
        "id,distance\n"
        "1,0\n"
        "2,0\n"
        "3,15\n"
        "4,1\n"
        "5,0\n"
        "6,0\n"
        "7,0\n"
        "8,0\n"
        "9,13\n"
        "10,0\n"
    )

    with open(output_path, 'r') as f:
        content = f.read()

    # Normalize line endings just in case
    content_lines = [line.strip() for line in content.strip().split('\n')]
    expected_lines = [line.strip() for line in expected_content.strip().split('\n')]

    assert content_lines == expected_lines, "The content of distances.csv does not match the expected output."

def test_cpp_file_exists():
    """Test that the C++ source file exists."""
    cpp_path = '/home/user/process_data.cpp'
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."