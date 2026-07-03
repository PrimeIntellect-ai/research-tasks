# test_final_state.py

import os
import pytest

def test_processed_data_exists_and_content():
    expected_file = "/home/user/processed_data.csv"
    assert os.path.exists(expected_file), f"Output file {expected_file} is missing."
    assert os.path.isfile(expected_file), f"Output path {expected_file} is not a file."

    expected_content = """record_id,dataset_split,norm_x,norm_y
1,train,-1.2247,-1.2247
4,train,0.0000,0.0000
5,test,-0.6124,0.6124
6,test,0.6124,1.2247
7,train,1.2247,1.2247"""

    with open(expected_file, "r") as f:
        actual_content = f.read()

    # Normalize line endings and strip trailing whitespaces
    actual_content = actual_content.replace("\r\n", "\n").strip()
    expected_content = expected_content.replace("\r\n", "\n").strip()

    assert actual_content == expected_content, (
        f"Content of {expected_file} does not match the expected processed data.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )

def test_script_exists():
    script_file = "/home/user/process_data.sh"
    assert os.path.exists(script_file), f"Script file {script_file} is missing."
    assert os.path.isfile(script_file), f"Script path {script_file} is not a file."