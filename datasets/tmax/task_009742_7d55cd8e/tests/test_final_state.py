# test_final_state.py
import os

def test_duplicates_csv_exists():
    """Check if the duplicates.csv file was created."""
    file_path = "/home/user/duplicates.csv"
    assert os.path.exists(file_path), f"The output file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_duplicates_csv_content():
    """Verify the contents of duplicates.csv exactly match the expected deduplication results."""
    expected_lines = [
        "P003,P004",
        "P005,P007",
        "P008,P009"
    ]

    file_path = "/home/user/duplicates.csv"
    assert os.path.exists(file_path), f"Cannot verify content, {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert lines == expected_lines, f"Expected output lines {expected_lines}, but got {lines}."

def test_cpp_source_exists():
    """Check if the student created the C++ source file."""
    file_path = "/home/user/dedup.cpp"
    assert os.path.exists(file_path), f"The C++ source file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_executable_exists():
    """Check if the compiled executable exists and is executable."""
    file_path = "/home/user/dedup"
    assert os.path.exists(file_path), f"The compiled executable {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."
    assert os.access(file_path, os.X_OK), f"The file {file_path} is not executable. Did you compile it?"