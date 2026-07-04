# test_final_state.py

import os
import pytest

def test_executable_exists():
    """Test that the compiled executable exists."""
    executable_path = "/home/user/generate_data"
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing. Did you compile the C file?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_hdf5_file_exists():
    """Test that the HDF5 data file exists."""
    data_path = "/home/user/data.h5"
    assert os.path.isfile(data_path), f"Data file {data_path} is missing. Did you run the compiled executable?"

def test_result_file_content():
    """Test that the result file exists and contains the correct Wasserstein distance."""
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "0.7321", f"Expected result '0.7321', but got '{content}'."