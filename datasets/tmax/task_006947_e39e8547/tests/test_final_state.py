# test_final_state.py

import os
import csv

def test_coauthors_csv_content():
    output_file = "/home/user/coauthors.csv"

    # Check if the output file exists
    assert os.path.isfile(output_file), f"Expected output file {output_file} does not exist."

    expected_lines = [
        "source,target",
        "Alice,Bob",
        "Alice,Charlie",
        "Alice,Dave",
        "Bob,Charlie",
        "Charlie,Eve",
        "Dave,Frank"
    ]

    with open(output_file, 'r', encoding='utf-8') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {output_file} does not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )

def test_script_exists():
    script_file = "/home/user/project_graph.sh"
    assert os.path.isfile(script_file), f"The script {script_file} does not exist."