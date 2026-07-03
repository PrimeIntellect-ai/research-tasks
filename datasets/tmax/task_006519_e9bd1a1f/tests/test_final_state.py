# test_final_state.py
import os
import pytest

def test_top_jobs_csv():
    file_path = "/home/user/top_jobs.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you run the compiled tool?"

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    expected = [
        "job_id,latency",
        "J1,35",
        "J2,35",
        "J4,35"
    ]

    assert content == expected, f"Content of {file_path} is incorrect. Expected {expected}, got {content}."

def test_top_hubs_csv():
    file_path = "/home/user/top_hubs.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you run the compiled tool?"

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    expected = [
        "node_id,degree",
        "B,3",
        "C,3",
        "A,2"
    ]

    assert content == expected, f"Content of {file_path} is incorrect. Expected {expected}, got {content}."