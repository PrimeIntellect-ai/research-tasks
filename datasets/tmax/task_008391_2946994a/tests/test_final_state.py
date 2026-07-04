# test_final_state.py

import os
import pytest

def test_extract_go_exists():
    path = "/home/user/extract.go"
    assert os.path.isfile(path), f"Expected Go program at {path} does not exist."

def test_sensor_A_extracted():
    path = "/home/user/extracted/sensor_A.csv"
    assert os.path.isfile(path), f"Expected extracted file {path} does not exist."

    expected_content = "timestamp,value\n1000,42.5\n1001,43.1\n"
    with open(path, "r") as f:
        content = f.read()
    assert content == expected_content, f"Content of {path} does not match expected."

def test_sensor_B_extracted():
    path = "/home/user/extracted/sensor_B.csv"
    assert os.path.isfile(path), f"Expected extracted file {path} does not exist."

    expected_content = "timestamp,value\n2000,12.5\n2001,13.1\n"
    with open(path, "r") as f:
        content = f.read()
    assert content == expected_content, f"Content of {path} does not match expected."

def test_sensor_C_not_extracted():
    path = "/home/user/extracted/sensor_C.csv"
    assert not os.path.exists(path), f"File {path} should not exist because its hash is corrupted."

def test_corrupted_log():
    path = "/home/user/corrupted.log"
    assert os.path.isfile(path), f"Expected log file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 1, f"Expected exactly 1 entry in {path}, found {len(lines)}."
    assert lines[0] == "sensor_C.csv", f"Expected 'sensor_C.csv' in {path}, got '{lines[0]}'."