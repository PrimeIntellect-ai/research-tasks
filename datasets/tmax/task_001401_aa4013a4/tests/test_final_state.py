# test_final_state.py
import os
import pytest

def test_cpp_file_exists():
    file_path = "/home/user/graph_optimizer.cpp"
    assert os.path.isfile(file_path), f"C++ source file missing: {file_path}"

def test_results_csv_exists_and_content():
    file_path = "/home/user/results.csv"
    assert os.path.isfile(file_path), f"Results file missing: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = """id,department,subtree_avg_salary,dept_rank
1,Engineering,88750,1
2,Engineering,87500,2
6,Engineering,85000,3
3,Engineering,80000,4
4,HR,65000,1
5,HR,60000,2
7,Sales,73333,1
8,Sales,50000,2
9,Sales,50000,2"""

    # Normalize line endings and compare
    content_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert content_lines == expected_lines, f"Content mismatch in {file_path}. Expected exactly the computed subtree average salaries and dense ranks."