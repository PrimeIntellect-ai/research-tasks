# test_final_state.py

import os
import pytest

def test_warehouse_index_exists_and_content():
    file_path = "/home/user/warehouse_index.csv"
    assert os.path.isfile(file_path), f"{file_path} is missing."

    expected_content = """Alpha,1
Beta,2
Delta,4
Echo,5
Gamma,3
Zeta,6"""

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {file_path} is incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_two_hop_alpha_exists_and_content():
    file_path = "/home/user/two_hop_Alpha.csv"
    assert os.path.isfile(file_path), f"{file_path} is missing."

    expected_content = """Destination_Name,Total_Cost
Delta,110
Delta,70
Echo,70"""

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {file_path} is incorrect. Expected:\n{expected_content}\nGot:\n{content}"