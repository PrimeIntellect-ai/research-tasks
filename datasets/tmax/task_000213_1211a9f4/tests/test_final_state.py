# test_final_state.py

import os
import json
import pytest

def test_backup_paths_json_exists():
    output_path = "/home/user/backup_paths.json"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist. Did you run the script?"
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_backup_paths_json_content():
    output_path = "/home/user/backup_paths.json"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} does not contain valid JSON.")

    # Expected paths of length 2: A->B and B->C, sorted.
    # Edges: (1,2), (2,3), (2,4), (4,5), (1,4)
    # Paths:
    # 1->2->3
    # 1->2->4
    # 1->4->5
    # 2->4->5

    expected_data = [
        [1, 2, 3],
        [1, 2, 4],
        [1, 4, 5],
        [2, 4, 5]
    ]

    # Convert tuples to lists if necessary, but json.load already produces lists for JSON arrays.
    data_as_lists = [list(row) for row in data]

    assert data_as_lists == expected_data, f"JSON data does not match the expected paths. Expected {expected_data}, but got {data_as_lists}."