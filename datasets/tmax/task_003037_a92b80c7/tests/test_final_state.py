# test_final_state.py

import os

def test_flag_file_exists_and_correct():
    flag_path = "/home/user/flag.txt"

    # Check if the file exists
    assert os.path.isfile(flag_path), f"The flag file {flag_path} does not exist. Did you successfully trigger the payload?"

    # Check the content of the file
    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_content = "PAYLOAD_UNLOCKED_77492"
    assert content == expected_content, f"The content of {flag_path} is incorrect. Expected '{expected_content}', but got '{content}'."