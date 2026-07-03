# test_final_state.py

import os

def test_significant_count_file_exists():
    """Test that the significant_count.txt file exists."""
    file_path = "/home/user/significant_count.txt"
    assert os.path.exists(file_path), f"The output file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a regular file."

def test_significant_count_value():
    """Test that the significant_count.txt contains the correct value."""
    output_path = "/home/user/significant_count.txt"
    expected_path = "/tmp/expected_count.txt"

    assert os.path.exists(output_path), f"The output file {output_path} is missing."
    assert os.path.exists(expected_path), f"The expected truth file {expected_path} is missing."

    with open(output_path, 'r') as f:
        student_output = f.read().strip()

    with open(expected_path, 'r') as f:
        expected_output = f.read().strip()

    assert student_output == expected_output, (
        f"The count in {output_path} is incorrect. "
        f"Expected '{expected_output}', but got '{student_output}'."
    )

def test_cpp_source_file_exists():
    """Test that the C++ source file exists."""
    file_path = "/home/user/calc_llr.cpp"
    assert os.path.exists(file_path), f"The source file {file_path} is missing. Did you write the C++ code?"
    assert os.path.isfile(file_path), f"{file_path} is not a regular file."