# test_final_state.py
import os

def test_total_salary_txt():
    path = "/home/user/total_salary.txt"
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert "475000" in content, f"Expected total salary 475000 in {path}, but found: {content}"

def test_aggregate_salary_cpp():
    path = "/home/user/aggregate_salary.cpp"
    assert os.path.isfile(path), f"Expected C++ source file {path} does not exist."

def test_hierarchy_json():
    path = "/home/user/hierarchy.json"
    assert os.path.isfile(path), f"Expected JSON output file {path} does not exist."