# test_final_state.py
import os

def test_libalgo_so_exists():
    path = "/home/user/polyglot/libalgo.so"
    assert os.path.isfile(path), f"Shared library {path} does not exist. Did you compile algo.c?"

def test_success_txt_exists_and_content():
    path = "/home/user/polyglot/success.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist. Did you run wrapper.py and save its output?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "2.0,3.0,4.0"
    assert expected in content, f"File {path} does not contain the expected output '{expected}'. Found: '{content}'"

def test_wrapper_py_fixes():
    path = "/home/user/polyglot/wrapper.py"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check that FFI signatures were added
    assert "argtypes" in content, "wrapper.py does not seem to define 'argtypes' for the C function."
    assert "restype" in content, "wrapper.py does not seem to define 'restype' for the C function."