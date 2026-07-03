# test_final_state.py

import os
import csv
import pytest

def test_c_source_exists():
    assert os.path.isfile('/home/user/analyzer.c'), "The C source file /home/user/analyzer.c is missing."

def test_output_csv_exists():
    assert os.path.isfile('/home/user/intra_institutional_citations.csv'), "The output CSV file /home/user/intra_institutional_citations.csv is missing."

def test_output_csv_content():
    expected_rows = [
        ['author_id', 'author_name', 'citing_paper_id', 'cited_paper_id', 'institution_id'],
        ['1', 'Alice', '101', '102', 'INST_A'],
        ['2', 'Bob', '105', '103', 'INST_B'],
        ['5', 'Eve', '103', '101', 'INST_B'],
        ['5', 'Eve', '103', '105', 'INST_B']
    ]

    with open('/home/user/intra_institutional_citations.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        actual_rows = [row for row in reader if row]

    assert actual_rows == expected_rows, f"The output CSV content does not match the expected output. Got: {actual_rows}"