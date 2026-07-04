# test_final_state.py

import os
import stat
import subprocess
import csv
import pytest

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_analyze_script_execution_and_output():
    script_path = "/home/user/analyze.sh"
    results_path = "/home/user/results.csv"

    # Remove results.csv if it exists to ensure we are testing the script's output
    if os.path.exists(results_path):
        os.remove(results_path)

    # Execute the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    assert os.path.exists(results_path), f"Output file {results_path} was not created."

    expected_rows = [
        ["emp_id", "name", "department", "salary", "management_level", "dept_avg_salary", "salary_rank_in_dept"],
        ["2", "Bob", "Engineering", "150000", "1", "115000", "1"],
        ["4", "David", "Engineering", "120000", "2", "115000", "2"],
        ["5", "Eve", "Engineering", "110000", "2", "115000", "3"],
        ["8", "Heidi", "Engineering", "80000", "3", "115000", "4"],
        ["1", "Alice", "Executive", "200000", "0", "200000", "1"],
        ["3", "Charlie", "Sales", "140000", "1", "110000", "1"],
        ["7", "Grace", "Sales", "100000", "2", "110000", "2"],
        ["6", "Frank", "Sales", "90000", "2", "110000", "3"]
    ]

    with open(results_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, "The output in results.csv does not match the expected data and ordering."