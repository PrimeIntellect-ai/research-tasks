# test_final_state.py
import os
import pytest

def test_eigenvector_file_exists():
    file_path = '/home/user/eigenvector.txt'
    assert os.path.exists(file_path), f"Expected output file {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_eigenvector_content():
    file_path = '/home/user/eigenvector.txt'
    assert os.path.exists(file_path), f"Expected output file {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected = "0.1171,0.0039,0.9931"
    assert content == expected, f"Expected eigenvector '{expected}', but got '{content}'"