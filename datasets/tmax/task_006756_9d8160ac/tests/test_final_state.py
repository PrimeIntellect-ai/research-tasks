# test_final_state.py

import os
import pytest

def test_recovered_sql_contains_data():
    recovered_path = "/home/user/recovered.sql"
    assert os.path.isfile(recovered_path), f"Expected recovered SQL file does not exist at {recovered_path}"

    with open(recovered_path, "r") as f:
        content = f.read()

    expected_values = ["1000000001.1", "1000000001.3", "1000000001.5"]
    for val in expected_values:
        assert val in content, f"Expected value {val} not found in {recovered_path}"

def test_variance_calculation():
    variance_path = "/home/user/variance.txt"
    assert os.path.isfile(variance_path), f"Expected variance output file does not exist at {variance_path}"

    with open(variance_path, "r") as f:
        content = f.read().strip()

    assert content == "0.0400", f"Expected variance to be '0.0400', but got '{content}'"