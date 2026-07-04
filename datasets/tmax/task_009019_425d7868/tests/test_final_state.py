# test_final_state.py
import os
import pytest

def test_result_txt_exists():
    assert os.path.isfile("/home/user/log_parser/result.txt"), "result.txt was not generated. Did you run `cargo run` after fixing the code?"

def test_result_txt_content():
    try:
        with open("/home/user/log_parser/result.txt", "r") as f:
            content = f.read().strip()
    except FileNotFoundError:
        pytest.fail("result.txt is missing.")

    assert content == "4500000000", f"Expected result.txt to contain '4500000000', but got '{content}'."

def test_rust_code_compiles_and_runs():
    # We can also check if the binary was built, but checking the result.txt is the primary requirement.
    pass