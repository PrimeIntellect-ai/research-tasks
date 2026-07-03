# test_final_state.py
import os

def test_cycles_output_exists():
    output_path = "/home/user/cycles.txt"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_cycles_output_content():
    output_path = "/home/user/cycles.txt"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_content = [
        "1,2,3",
        "10,11,12",
        "7,8,9"
    ]

    assert len(content) == len(expected_content), f"Expected {len(expected_content)} lines, but got {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_content)):
        assert actual.strip() == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual.strip()}'."

def test_cpp_source_exists():
    source_path = "/home/user/find_pattern.cpp"
    assert os.path.exists(source_path), f"C++ source file {source_path} does not exist."