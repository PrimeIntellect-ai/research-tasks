# test_final_state.py

import os
import stat
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/query_graph.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable"

def test_results_csv_exists_and_correct():
    results_path = "/home/user/results.csv"
    assert os.path.isfile(results_path), f"Results file not found at {results_path}"

    expected_content = """user_id,user_name,product_id,product_name,purchase_date
U3,Charlie,P4,Smartphone,2023-10-10
U2,Bob,P1,Laptop,2023-10-02
U1,Alice,P1,Laptop,2023-10-01"""

    with open(results_path, 'r') as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {results_path} does not match expected output.\nExpected:\n{expected_content}\n\nActual:\n{content}"