# test_final_state.py
import os
import re

def test_cpp_source_exists():
    path = "/home/user/reducer.cpp"
    assert os.path.isfile(path), f"{path} does not exist."

def test_executable_exists():
    path = "/home/user/reducer"
    assert os.path.isfile(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_reduced_csv_content():
    path = "/home/user/reduced.csv"
    assert os.path.isfile(path), f"{path} does not exist."

    expected = """3,7,11,15,19
30,70,110,150,190
0,7,6,7,9
0,0,0,0,0
0,0,0,0,0
1000,2000,3000,4000,5000"""

    with open(path, "r") as f:
        actual = f.read().strip()

    assert actual == expected, "The contents of reduced.csv do not match the expected dimensionality reduction and imputation."

def test_benchmark_txt():
    path = "/home/user/benchmark.txt"
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert re.match(r'^[0-9]+(\.[0-9]+)?$', content), f"benchmark.txt does not contain a valid number, got: {content}"