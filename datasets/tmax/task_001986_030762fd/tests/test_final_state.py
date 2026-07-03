# test_final_state.py

import os
import pytest

def test_stats_h_recovered():
    file_path = "/home/user/stats_project/stats.h"
    assert os.path.isfile(file_path), f"{file_path} is missing. Did you recover it from git?"

def test_makefile_fixed():
    file_path = "/home/user/stats_project/Makefile"
    assert os.path.isfile(file_path), f"{file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read()
    assert "-llegacy" not in content, "Makefile still contains '-llegacy'. You must remove it to resolve the symbol conflict."
    assert "-ladvanced" in content, "Makefile must still link against '-ladvanced'."

def test_executable_exists():
    file_path = "/home/user/stats_project/calc_variance"
    assert os.path.isfile(file_path), f"Executable {file_path} is missing. Did you compile the application?"
    assert os.access(file_path, os.X_OK), f"{file_path} is not executable."

def test_final_result():
    file_path = "/home/user/stats_project/final_result.txt"
    assert os.path.isfile(file_path), f"{file_path} is missing. Did you run the program and redirect the output?"
    with open(file_path, "r") as f:
        content = f.read().strip()
    assert content == "8.0000", f"Expected '8.0000' in {file_path}, but got '{content}'."