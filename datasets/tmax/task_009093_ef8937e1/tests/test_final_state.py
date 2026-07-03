# test_final_state.py
import os
import pytest

def test_eigen_directory_exists():
    """Test that the eigen directory was created."""
    assert os.path.isdir("/home/user/eigen"), "/home/user/eigen directory is missing. You must download and extract the Eigen library here."

def test_executable_exists():
    """Test that the recommender script was compiled into an executable."""
    assert os.path.isfile("/home/user/recommender"), "The compiled executable /home/user/recommender is missing."
    assert os.access("/home/user/recommender", os.X_OK), "/home/user/recommender is not executable."

def test_output_file_exists_and_correct():
    """Test that the output file contains the expected recommendations."""
    output_path = "/home/user/output.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} is missing. Did the script run successfully?"

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected = "10: 11, 13, 14"
    assert content == expected, f"Expected output '{expected}', but got '{content}'."