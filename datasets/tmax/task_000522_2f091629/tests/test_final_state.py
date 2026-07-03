# test_final_state.py

import os

def test_recovered_data_exists_and_correct():
    file_path = "/home/user/recovered_data.txt"
    assert os.path.exists(file_path), f"The file {file_path} does not exist. The task requires writing the recovered strings to this file."

    with open(file_path, "r", encoding="utf-8") as f:
        # Read lines, strip whitespace/newlines, and ignore completely empty lines
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "USER_1=ALICE",
        "USER_2=BOB",
        "USER_3=CHARLIE",
        "USER_4=DAVE",
        "USER_5=EVE"
    ]

    assert lines == expected_lines, (
        f"The content of {file_path} does not match the expected recovered records.\n"
        f"Expected: {expected_lines}\n"
        f"Found: {lines}"
    )