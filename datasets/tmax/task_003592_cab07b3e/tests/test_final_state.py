# test_final_state.py
import os

def test_generator_executable_exists():
    path = "/home/user/generator"
    assert os.path.isfile(path), f"Executable {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_samples_txt_exists():
    path = "/home/user/samples.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip().split()

    assert len(content) == 7, f"Expected 7 samples in {path}, found {len(content)}."

def test_fit_py_exists():
    path = "/home/user/fit.py"
    assert os.path.isfile(path), f"File {path} is missing."

def test_result_txt_correct():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "a=-1.649"
    assert content == expected, f"Expected result.txt to contain '{expected}', but found '{content}'."