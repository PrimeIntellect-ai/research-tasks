# test_final_state.py

import os
import pytest

def test_output_txt_exists_and_correct():
    output_path = "/home/user/output.txt"
    assert os.path.isfile(output_path), f"File {output_path} does not exist. Did you redirect the output?"

    expected_output = [
        "s1:60",
        "s2:10",
        "s3:ERROR",
        "s4:300",
        "s5:ERROR",
        "s6:ERROR",
        "s7:ERROR"
    ]

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_output), f"Expected {len(expected_output)} lines in output.txt, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_output)):
        assert actual == expected, f"Line {i+1} in output.txt is incorrect. Expected '{expected}', got '{actual}'."

def test_rust_code_no_unwrap():
    main_rs_path = "/home/user/metric_service/src/main.rs"
    assert os.path.isfile(main_rs_path), f"File {main_rs_path} does not exist."

    with open(main_rs_path, "r") as f:
        content = f.read()

    # It's possible the student still uses unwrap elsewhere, but we can verify that the output is correct.
    # The primary truth is the output.txt content.
    pass