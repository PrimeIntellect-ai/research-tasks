# test_final_state.py

import os
import pytest

def test_window_results_exists_and_correct():
    """Test that window_results.csv exists and has the correct content."""
    file_path = "/home/user/window_results.csv"
    assert os.path.isfile(file_path), f"The required output file {file_path} does not exist."

    expected_lines = [
        "A,F,20,1",
        "A,B,10,2",
        "A,H,10,2",
        "B,D,8,1",
        "C,D,15,1",
        "D,E,2,1",
        "F,G,1,1",
        "H,I,12,1"
    ]

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"Content of {file_path} is incorrect. Expected: {expected_lines}, but got: {lines}"

def test_graph_results_exists_and_correct():
    """Test that graph_results.csv exists and has the correct content."""
    file_path = "/home/user/graph_results.csv"
    assert os.path.isfile(file_path), f"The required output file {file_path} does not exist."

    expected_lines = [
        "D,8",
        "G,1",
        "I,10"
    ]

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"Content of {file_path} is incorrect. Expected: {expected_lines}, but got: {lines}"

def test_cpp_source_exists():
    """Test that the C++ source file exists."""
    assert os.path.isfile("/home/user/process_network.cpp"), "The C++ source file /home/user/process_network.cpp does not exist."

def test_cpp_executable_exists():
    """Test that the C++ executable exists."""
    assert os.path.isfile("/home/user/process_network"), "The compiled executable /home/user/process_network does not exist."
    assert os.access("/home/user/process_network", os.X_OK), "The file /home/user/process_network is not executable."