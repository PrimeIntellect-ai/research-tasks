# test_final_state.py

import os
import pytest

def test_dataset_v1_content():
    file_path = "/home/user/dataset_v1.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you save the output dataset?"

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "ts,f1,f2,f3,error,ratio,y",
        "1,10.5,2.0,9.0,1.5000,0.7500,1",
        "2,11.0,0.0,11.0,0.0000,0.0000,0",
        "3,9.5,1.5,10.0,-0.5000,-0.3333,1",
        "4,12.1,3.0,10.0,2.1000,0.7000,1",
        "5,8.0,2.0,7.8,0.2000,0.1000,0"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {file_path} is incorrect.\nExpected: {expected}\nActual:   {actual}"

def test_metrics_content():
    file_path = "/home/user/metrics.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you save the metrics file?"

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Total_Samples=5",
        "Positive_Class_Ratio=0.6000",
        "Mean_Error=0.6600"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {file_path} is incorrect.\nExpected: {expected}\nActual:   {actual}"