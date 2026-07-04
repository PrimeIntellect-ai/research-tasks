# test_final_state.py
import os
import re

SCRIPT_PATH = '/home/user/compile_dataset.sh'
OUTPUT_PATH = '/home/user/clean_dataset.txt'

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_contains_required_commands():
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()

    assert "mktemp" in content, "Script does not contain 'mktemp' for secure temporary file creation."

    # Check for atomic move to the final destination
    assert re.search(r"mv\s+.*clean_dataset\.txt", content) is not None, "Script does not contain an atomic 'mv' command to the final destination."

def test_output_file_contents():
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."

    with open(OUTPUT_PATH, 'r') as f:
        actual_lines = f.read().splitlines()

    expected_lines = [
        "[RETAIN] data_point_1",
        "[RETAIN] data_point_2",
        "[RETAIN] data_point_5",
        "[RETAIN] data_point_7"
    ]

    assert actual_lines == expected_lines, f"Contents of {OUTPUT_PATH} do not match the expected sorted output. Got: {actual_lines}"