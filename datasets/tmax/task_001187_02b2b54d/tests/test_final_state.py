# test_final_state.py
import os
import re
import pytest

def test_etl_script_exists_and_executable():
    script_path = "/home/user/etl.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_csv_output():
    csv_path = "/home/user/high_value_users.csv"
    assert os.path.isfile(csv_path), f"{csv_path} does not exist."

    expected_csv = "user_id,name,total_spent\n2,Bob,200\n1,Alice,160"

    with open(csv_path, "r") as f:
        actual_csv = f.read().strip().replace("\r", "")

    assert actual_csv == expected_csv, (
        f"CSV content does not match expected output.\n"
        f"Expected:\n{expected_csv}\n"
        f"Actual:\n{actual_csv}"
    )

def test_mongo_index():
    index_path = "/home/user/mongo_index.js"
    assert os.path.isfile(index_path), f"{index_path} does not exist."

    with open(index_path, "r") as f:
        content = f.read()

    # Normalize content: remove whitespace, tabs, newlines, and convert single quotes to double quotes
    normalized_content = re.sub(r'\s+', '', content).replace("'", '"')

    assert '"status":1' in normalized_content or '"status":-1' in normalized_content, (
        "mongo_index.js does not contain an index on 'status'."
    )
    assert '"user_id":1' in normalized_content or '"user_id":-1' in normalized_content, (
        "mongo_index.js does not contain an index on 'user_id'."
    )
    assert "createIndex" in normalized_content, (
        "mongo_index.js does not contain a createIndex command."
    )