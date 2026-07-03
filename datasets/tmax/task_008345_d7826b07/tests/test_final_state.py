# test_final_state.py
import os

def test_outliers_file_exists():
    path = "/home/user/outliers.txt"
    assert os.path.isfile(path), f"The file {path} does not exist. Make sure you saved your output to the correct location."

def test_outliers_content():
    path = "/home/user/outliers.txt"
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "10", f"Expected outlier ID '10', but got '{content}'. Please verify your joining, math, and threshold calculations."