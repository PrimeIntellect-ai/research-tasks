# test_final_state.py

import os
import json

def test_analysis_notebook_exists():
    path = "/home/user/analysis.ipynb"
    assert os.path.isfile(path), f"Missing file: {path}"

    # Basic check to see if it's a valid JSON/Notebook
    try:
        with open(path, 'r') as f:
            nb = json.load(f)
        assert "cells" in nb, f"Invalid notebook format in {path}: missing 'cells'"
    except json.JSONDecodeError:
        assert False, f"File {path} is not a valid JSON/Jupyter notebook."

def test_variance_comparison_png_exists():
    path = "/home/user/variance_comparison.png"
    assert os.path.isfile(path), f"Missing file: {path}"
    assert os.path.getsize(path) > 0, f"File {path} is empty."

    # Check PNG magic number
    with open(path, 'rb') as f:
        header = f.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', f"File {path} is not a valid PNG image."

def test_converged_w_txt_content():
    path = "/home/user/converged_W.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "60", f"Expected converged_W.txt to contain '60', but got '{content}'."