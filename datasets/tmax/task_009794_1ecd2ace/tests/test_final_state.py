# test_final_state.py

import os
import pytest

def test_c_source_exists():
    source_file = "/home/user/spectral_analysis.c"
    assert os.path.isfile(source_file), f"C source file {source_file} does not exist."

def test_executable_exists():
    executable = "/home/user/analyzer"
    assert os.path.isfile(executable), f"Executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_peak_frequency_output():
    output_file = "/home/user/peak_frequency.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        content = f.read().strip()

    assert content == "15", f"Expected peak frequency to be 15, but got '{content}'."