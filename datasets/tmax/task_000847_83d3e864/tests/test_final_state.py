# test_final_state.py

import os
import pytest

def test_etl_script_exists_and_executable():
    script_path = "/home/user/etl.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_manager_summary_csv_content():
    output_path = "/home/user/manager_summary.csv"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist. Did you run the script?"

    expected_content = """manager_id,manager_name,department,direct_reports_count,total_descendant_salary
1,Alice,Exec,2,780000
2,Bob,Engineering,2,330000
3,Charlie,Engineering,1,100000
5,Eve,Sales,1,170000
6,Frank,Sales,1,80000"""

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, (
        f"The content of {output_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n\nGot:\n{content}"
    )