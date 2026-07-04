# test_final_state.py
import os
import pytest

def test_output_file_exists():
    assert os.path.isfile("/home/user/collatz/output.txt"), "The file /home/user/collatz/output.txt does not exist. Did you run the Go program?"

def test_output_file_content():
    expected_lines = [
        "Input: 12, Steps: 9",
        "Input: 15, Steps: 17",
        "Input: -5, Steps: Invalid",
        "Input: 27, Steps: 111",
        "Input: 0, Steps: Invalid",
        "Input: 9, Steps: 19"
    ]

    output_path = "/home/user/collatz/output.txt"
    assert os.path.isfile(output_path), "Missing output.txt"

    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of /home/user/collatz/output.txt are incorrect.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )

def test_main_go_modified():
    main_go_path = "/home/user/collatz/main.go"
    assert os.path.isfile(main_go_path), "The file /home/user/collatz/main.go does not exist."

    with open(main_go_path, "r") as f:
        content = f.read()

    assert "-1" in content, "The collatzSteps function does not seem to return -1 for non-positive inputs."
    assert "Invalid" in content, "The main function does not seem to print 'Invalid' for non-positive inputs."