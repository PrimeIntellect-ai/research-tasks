# test_final_state.py

import os
import pytest

def test_train_processed():
    path = "/home/user/train_processed.csv"
    assert os.path.exists(path), f"{path} does not exist. The C program may not have run successfully or written the file."

    with open(path, 'r') as f:
        content = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    expected = [
        "-1.3229,-1.7008",
        "-0.5669,0.0000",
        "0.1890,-0.1890",
        "0.0000,0.5669",
        "1.7008,1.3229"
    ]

    assert len(content) == len(expected), f"Output line count mismatch in {path}: expected {len(expected)}, got {len(content)}"
    for i, (act, exp) in enumerate(zip(content, expected)):
        # Allow optional spaces after comma
        act_clean = act.replace(" ", "")
        exp_clean = exp.replace(" ", "")
        assert act_clean == exp_clean, f"Mismatch on line {i+1} in {path}: expected {exp}, got {act}"

def test_test_processed():
    path = "/home/user/test_processed.csv"
    assert os.path.exists(path), f"{path} does not exist. The C program may not have run successfully or written the file."

    with open(path, 'r') as f:
        content = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    expected = [
        "-0.9449,-0.9449",
        "0.0000,-0.5669",
        "1.3229,0.0000"
    ]

    assert len(content) == len(expected), f"Output line count mismatch in {path}: expected {len(expected)}, got {len(content)}"
    for i, (act, exp) in enumerate(zip(content, expected)):
        # Allow optional spaces after comma
        act_clean = act.replace(" ", "")
        exp_clean = exp.replace(" ", "")
        assert act_clean == exp_clean, f"Mismatch on line {i+1} in {path}: expected {exp}, got {act}"