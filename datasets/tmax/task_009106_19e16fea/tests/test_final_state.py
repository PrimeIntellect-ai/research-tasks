# test_final_state.py

import os
import pytest

def test_predictions_txt_content():
    predictions_path = "/home/user/predictions.txt"
    assert os.path.exists(predictions_path), f"File {predictions_path} does not exist."

    with open(predictions_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in predictions.txt, found {len(lines)}."
    assert lines[0] == "1", f"Expected first prediction to be '1', got '{lines[0]}'."
    assert lines[1] == "0", f"Expected second prediction to be '0', got '{lines[1]}'."

def test_cpp_file_exists():
    cpp_path = "/home/user/classifier.cpp"
    assert os.path.exists(cpp_path), f"Source file {cpp_path} does not exist."

def test_executable_exists():
    exe_path = "/home/user/classifier"
    assert os.path.exists(exe_path), f"Compiled executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."