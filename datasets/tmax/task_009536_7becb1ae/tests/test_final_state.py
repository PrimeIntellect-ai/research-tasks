# test_final_state.py
import os

def test_process_script_exists_and_executable():
    path = "/home/user/process.sh"
    assert os.path.exists(path), f"Bash script {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"Bash script {path} is not executable."

def test_c_source_exists():
    path = "/home/user/distance.c"
    assert os.path.exists(path), f"C source file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_c_binary_exists_and_executable():
    path = "/home/user/distance_calc"
    assert os.path.exists(path), f"Compiled C binary {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"Compiled C binary {path} is not executable."

def test_valid_distances_output():
    path = "/home/user/valid_distances.txt"
    assert os.path.exists(path), f"Final output file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1620000000 0.00",
        "1620000002 5.00",
        "1620000007 5.00"
    ]

    assert lines == expected_lines, f"Contents of {path} do not match the expected output. Got: {lines}, Expected: {expected_lines}"