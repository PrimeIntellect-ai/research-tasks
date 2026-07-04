# test_final_state.py

import os
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Fail: {script_path} not found"
    assert os.access(script_path, os.X_OK), f"Fail: {script_path} is not executable"

def test_posteriors_csv_exists_and_correct():
    csv_path = "/home/user/posteriors.csv"
    assert os.path.isfile(csv_path), f"Fail: {csv_path} not found"

    expected_content = (
        "srv_06,0.0802\n"
        "srv_01,0.0625\n"
        "srv_10,0.0625\n"
        "srv_09,0.0430\n"
        "srv_02,0.0323"
    )

    with open(csv_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Fail: Content of {csv_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )