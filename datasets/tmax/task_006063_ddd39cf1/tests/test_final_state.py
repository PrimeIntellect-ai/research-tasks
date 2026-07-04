# test_final_state.py
import os

def test_xor_key_file():
    path = "/home/user/xor_key.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip().lower()
    assert content == "0x42", f"Expected '0x42' in {path}, but found '{content}'."

def test_final_output_file():
    path = "/home/user/final_output.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "ALFA",
        "BRAVO",
        "CHARLIE",
        "DELTA",
        "ECHO",
        "FOXTROT",
        "GOLF",
        "HOTEL",
        "INDIA",
        "JULIETT"
    ]

    assert lines == expected_lines, f"Content of {path} does not match the expected sorted output. Found: {lines}"

def test_process_data_concurrent():
    path = "/home/user/process_data.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "&" in content, f"The script {path} must use '&' for concurrent processing."