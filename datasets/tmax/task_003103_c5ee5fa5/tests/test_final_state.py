# test_final_state.py

import os
import pytest

def test_summary_file_exists_and_content():
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"Summary file {summary_path} does not exist."

    with open(summary_path, "r") as f:
        content = f.read().strip()

    expected_content = "Positive: 27\nNegative: 23"
    assert content == expected_content, f"Summary file content is incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_dataset_directory_is_empty():
    dataset_path = "/home/user/dataset"
    assert os.path.isdir(dataset_path), f"Directory {dataset_path} does not exist."
    files = os.listdir(dataset_path)
    assert len(files) == 0, f"Directory {dataset_path} is not empty. Found {len(files)} files."

def test_positive_cases_directory_contents():
    pos_path = "/home/user/positive_cases"
    assert os.path.isdir(pos_path), f"Directory {pos_path} does not exist."
    files = os.listdir(pos_path)
    npy_files = [f for f in files if f.endswith('.npy')]
    assert len(npy_files) == 27, f"Expected 27 .npy files in {pos_path}, found {len(npy_files)}."

def test_negative_cases_directory_contents():
    neg_path = "/home/user/negative_cases"
    assert os.path.isdir(neg_path), f"Directory {neg_path} does not exist."
    files = os.listdir(neg_path)
    npy_files = [f for f in files if f.endswith('.npy')]
    assert len(npy_files) == 23, f"Expected 23 .npy files in {neg_path}, found {len(npy_files)}."

def test_total_files_moved():
    pos_path = "/home/user/positive_cases"
    neg_path = "/home/user/negative_cases"

    pos_files = os.listdir(pos_path) if os.path.isdir(pos_path) else []
    neg_files = os.listdir(neg_path) if os.path.isdir(neg_path) else []

    total_files = len(pos_files) + len(neg_files)
    assert total_files == 50, f"Expected a total of 50 files moved, but found {total_files}."