# test_final_state.py

import os

def test_output_file_exists():
    output_file = "/home/user/project/output.txt"
    assert os.path.isfile(output_file), f"Expected output file {output_file} does not exist. Did you run 'make test'?"

def test_output_content_correct():
    output_file = "/home/user/project/output.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    expected_output = "Read: Hello\nRead: C++\nRead: Café\nRead: World"

    with open(output_file, "r", encoding="utf-8") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_output, (
        f"The content of {output_file} is incorrect.\n"
        f"Expected:\n{expected_output}\n\n"
        f"Actual:\n{actual_content}\n\n"
        "Ensure your C++ code correctly reads the number of UTF-8 characters, not bytes."
    )