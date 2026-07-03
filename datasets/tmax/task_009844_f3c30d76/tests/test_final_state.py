# test_final_state.py
import os
import pytest

def test_final_output_exists():
    assert os.path.isfile("/home/user/final_output.txt"), "/home/user/final_output.txt is missing. Did you run the pipeline script?"

def test_final_output_content():
    expected_content = (
        "data_01.csv,335.000000\n"
        "data_02.csv,50.000000\n"
        "data_03.csv,10.000000"
    )

    with open("/home/user/final_output.txt", "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of /home/user/final_output.txt is incorrect or not sorted properly.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{actual_content}"
    )