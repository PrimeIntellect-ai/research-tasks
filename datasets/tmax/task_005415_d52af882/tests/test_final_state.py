# test_final_state.py

import os
import csv
import pytest

def test_top_items_exists():
    output_path = '/home/user/top_items.csv'
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist. Did your Go program write to the correct path?"

def test_top_items_content():
    output_path = '/home/user/top_items.csv'
    expected_path = '/home/user/expected_top_items.csv'

    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."
    assert os.path.isfile(expected_path), f"The expected output file {expected_path} is missing."

    with open(output_path, 'r', newline='') as f:
        reader = csv.reader(f)
        output_rows = list(reader)

    with open(expected_path, 'r', newline='') as f:
        reader = csv.reader(f)
        expected_rows = list(reader)

    assert len(output_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in {output_path}, but found {len(output_rows)}."

    for i, (out_row, exp_row) in enumerate(zip(output_rows, expected_rows)):
        assert len(out_row) == 2, f"Row {i+1} in {output_path} does not have exactly 2 columns: {out_row}"

        out_item, out_sim = out_row
        exp_item, exp_sim = exp_row

        assert out_item == exp_item, f"Row {i+1}: Expected item '{exp_item}', but got '{out_item}'."
        assert out_sim == exp_sim, f"Row {i+1}: Expected similarity '{exp_sim}' for item '{exp_item}', but got '{out_sim}'."