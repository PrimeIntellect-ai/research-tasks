# test_final_state.py

import os
import re
import pytest

def test_cleaned_dataset():
    path = '/home/user/cleaned_dataset.csv'
    assert os.path.isfile(path), f"File missing: {path}"

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "id,value1,value2,value3",
        "1,0.5,2.0,1.0",
        "-1,1.0,1.0,1.0",
        "3,0.0,3.0,0.0",
        "4,2.0,-1.0,-2.0"
    ]

    assert lines == expected_lines, f"Content of {path} does not match expected."

def test_inference_script_exists():
    path = '/home/user/inference.py'
    assert os.path.isfile(path), f"File missing: {path}"

def test_predictions():
    path = '/home/user/predictions.csv'
    assert os.path.isfile(path), f"File missing: {path}"

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "id,prediction",
        "1,0",
        "-1,1",
        "3,0",
        "4,1"
    ]

    assert lines == expected_lines, f"Content of {path} does not match expected."

def test_accuracy_txt():
    path = '/home/user/accuracy.txt'
    assert os.path.isfile(path), f"File missing: {path}"

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "2.0798", f"Content of {path} is '{content}', expected '2.0798'."

def test_benchmark_txt():
    path = '/home/user/benchmark.txt'
    assert os.path.isfile(path), f"File missing: {path}"

    with open(path, 'r') as f:
        content = f.read().strip()

    # Check if the last line or any line matches the format
    lines = content.split('\n')
    found = False
    for line in lines:
        if re.search(r'Average:\s+\d+\.\d+\s+seconds', line):
            found = True
            break

    assert found, f"Could not find required format 'Average: X.XXXX seconds' in {path}."