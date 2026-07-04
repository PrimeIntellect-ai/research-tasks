# test_final_state.py
import os

def test_best_match_file_exists():
    """Check that the best_match.txt file was created."""
    file_path = "/home/user/best_match.txt"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

def test_best_match_content():
    """Check that the best_match.txt file contains the correct ticket ID."""
    file_path = "/home/user/best_match.txt"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "105", f"Expected '105' in {file_path}, but got '{content}'."