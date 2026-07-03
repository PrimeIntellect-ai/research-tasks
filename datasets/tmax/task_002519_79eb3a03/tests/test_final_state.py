# test_final_state.py

import os

def test_clean_data_csv():
    file_path = "/home/user/clean_data.csv"
    assert os.path.exists(file_path), f"The file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    expected_content = """timestamp,sensor_A,sensor_B
t1,10.0,20.0
t2,12.0,25.0
t4,9.0,19.0
t5,15.0,31.0
t6,14.0,27.0
t7,16.0,33.0
t9,8.0,16.0
t11,11.0,22.0"""

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"The content of {file_path} does not match the expected cleaned data."

def test_correlation_txt():
    file_path = "/home/user/correlation.txt"
    assert os.path.exists(file_path), f"The file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "0.9960", f"The correlation value in {file_path} is expected to be '0.9960', but got '{content}'."