# test_final_state.py

import os

def test_cpp_source_exists():
    path = "/home/user/analyze_config.cpp"
    assert os.path.exists(path), f"Source file {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_executable_exists():
    path = "/home/user/analyze_config"
    assert os.path.exists(path), f"Executable {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_output_file_contents():
    path = "/home/user/closest_server.txt"
    assert os.path.exists(path), f"Output file {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "server_077,0.8182"
    assert content == expected, f"Output file content is incorrect. Expected '{expected}', got '{content}'."