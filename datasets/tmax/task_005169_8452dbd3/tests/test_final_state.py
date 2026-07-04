# test_final_state.py

import os

def test_linker_flags_file_exists():
    assert os.path.isfile("/home/user/linker_flags.txt"), "The /home/user/linker_flags.txt file is missing."

def test_linker_flags_content():
    expected_lines = [
        "/home/user/libs/libcore.so.1.2.0",
        "/home/user/libs/libmath.so.3.1.4",
        "/home/user/libs/libnet.so.1.2.4"
    ]

    with open("/home/user/linker_flags.txt", "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of /home/user/linker_flags.txt do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )