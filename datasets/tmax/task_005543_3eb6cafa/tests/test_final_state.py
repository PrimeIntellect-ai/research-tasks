# test_final_state.py

import os

def test_rust_file_exists():
    rs_path = "/home/user/detector.rs"
    assert os.path.isfile(rs_path), f"Expected Rust source file {rs_path} does not exist."

def test_deadlock_txt_correct():
    txt_path = "/home/user/deadlock.txt"
    assert os.path.isfile(txt_path), f"Expected output file {txt_path} does not exist."

    with open(txt_path, "r") as f:
        content = f.read().strip()

    expected_content = "200,201,202,203,204,205"
    assert content == expected_content, f"Content of {txt_path} is incorrect. Expected '{expected_content}', got '{content}'."