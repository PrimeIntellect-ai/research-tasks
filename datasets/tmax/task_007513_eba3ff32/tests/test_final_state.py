# test_final_state.py
import os
import re

def test_go_mod_exists():
    path = "/home/user/go.mod"
    assert os.path.isfile(path), f"File {path} is missing. Did you initialize the Go module?"

def test_trace_txt_exists_and_valid():
    path = "/home/user/trace.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did the script run successfully?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content, f"File {path} is empty."

    try:
        val = float(content)
    except ValueError:
        assert False, f"Content of {path} is not a valid floating-point number: {content}"

def test_generate_go_modified():
    path = "/home/user/generate.go"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check that some form of ridge addition is present
    # Could be cov.SetSym(i, i, cov.At(i, i) + 1e-4) or similar
    # We check if 1e-4 or 0.0001 is in the file
    has_ridge = "1e-4" in content or "0.0001" in content or ".0001" in content
    assert has_ridge, f"File {path} does not seem to contain the ridge value 1e-4 or 0.0001."