# test_final_state.py

import os
import glob
import pytest

def test_cython_extension_compiled():
    """Check if the Cython extension was compiled in-place."""
    # Look for the compiled shared object file
    so_files = glob.glob("/home/user/calc_chunk.*.so")
    assert len(so_files) > 0, "The Cython extension calc_chunk.pyx does not appear to be compiled. Missing .so file."

def test_result_txt_exists():
    """Check if the result.txt file was created."""
    assert os.path.isfile("/home/user/result.txt"), "The file /home/user/result.txt is missing."

def test_result_matches_reference():
    """Check if the content of result.txt matches reference.txt exactly (ignoring whitespace)."""
    ref_path = "/home/user/reference.txt"
    res_path = "/home/user/result.txt"

    assert os.path.isfile(ref_path), f"Missing reference file: {ref_path}"
    assert os.path.isfile(res_path), f"Missing result file: {res_path}"

    with open(ref_path, 'r') as f:
        ref_val = f.read().strip()

    with open(res_path, 'r') as f:
        res_val = f.read().strip()

    assert res_val == ref_val, f"The value in result.txt ('{res_val}') does not match the reference value ('{ref_val}')."