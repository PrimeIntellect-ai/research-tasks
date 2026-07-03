# test_final_state.py

import os

def test_libframing_so_exists():
    path = "/home/user/libframing.so"
    assert os.path.isfile(path), f"File {path} is missing. Did you compile the Rust code?"

def test_frame_output_hex_content():
    path = "/home/user/frame_output.hex"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the Python script?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "820454455354"
    assert content == expected, f"Expected {path} to contain '{expected}', but got '{content}'."

def test_fuzzer_py_exists():
    path = "/home/user/fuzzer.py"
    assert os.path.isfile(path), f"File {path} is missing."

def test_framing_rs_exists():
    path = "/home/user/framing.rs"
    assert os.path.isfile(path), f"File {path} is missing."