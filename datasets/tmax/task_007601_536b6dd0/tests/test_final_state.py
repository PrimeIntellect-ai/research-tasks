# test_final_state.py

import os
import pytest

def test_etl_go_exists():
    etl_go_path = "/home/user/etl.go"
    assert os.path.exists(etl_go_path), f"File {etl_go_path} is missing."
    assert os.path.isfile(etl_go_path), f"Path {etl_go_path} is not a file."

def test_clean_data_exists_and_content():
    clean_data_path = "/home/user/clean_data.csv"

    # Check if the file exists
    assert os.path.exists(clean_data_path), f"File {clean_data_path} is missing. The Go script might not have been run or failed to produce output."
    assert os.path.isfile(clean_data_path), f"Path {clean_data_path} is not a file."

    expected_content = (
        "metric_A,metric_C\n"
        "1.0,1.0\n"
        "2.0,0.0\n"
        "4.0,0.0\n"
        "5.0,1.0"
    )

    with open(clean_data_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {clean_data_path} does not match the expected final state. Expected:\n{expected_content}\nGot:\n{content}"