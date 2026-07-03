# test_final_state.py

import os
import pytest

def test_analyze_script_exists():
    script_path = "/home/user/analyze.py"
    assert os.path.exists(script_path), f"The script {script_path} was not created."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_top_warehouses_csv_exists_and_correct():
    output_path = "/home/user/top_warehouses.csv"
    assert os.path.exists(output_path), f"The output file {output_path} was not created."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

    expected_content = """warehouse_id,urgency_score
WH-02,300.00
WH-05,250.00
WH-04,80.00"""

    with open(output_path, "r") as f:
        content = f.read().strip()

    # Normalize line endings just in case
    content_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert content_lines == expected_lines, (
        f"The content of {output_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )