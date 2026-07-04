# test_final_state.py

import os
import re

def test_consolidate_script_exists():
    script_path = "/home/user/consolidate.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_output_file_exists():
    output_path = "/home/user/critical_errors.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist. Did the script run successfully?"

def test_output_file_content():
    output_path = "/home/user/critical_errors.txt"
    if not os.path.isfile(output_path):
        return # Handled by previous test

    with open(output_path, "r") as f:
        actual_content = f.read()

    expected_content = """[2023-10-01 10:10:00] FATAL CRITICAL_FAILURE: DB connection lost
    at db.connect()
    at main()
---END_RECORD---
[2023-10-04 13:00:00] FATAL CRITICAL_FAILURE: Network timeout
    Retries: 5
    Status: Failed
---END_RECORD---
[2023-10-02 11:05:00] FATAL CRITICAL_FAILURE: Out of memory
    Heap dump:
    0x0001
    0x0002
---END_RECORD---
"""

    # Normalize newlines just in case
    actual_content = actual_content.replace("\r\n", "\n")
    expected_content = expected_content.replace("\r\n", "\n")

    assert actual_content == expected_content, f"The content of {output_path} does not match the expected output. Found:\n{actual_content}"

def test_script_uses_atomic_write():
    script_path = "/home/user/consolidate.py"
    if not os.path.isfile(script_path):
        return

    with open(script_path, "r") as f:
        script_content = f.read()

    # Check if there is some rename or move logic indicating atomic write
    has_rename = re.search(r'(os\.rename|shutil\.move|Path\.rename)', script_content)
    has_tmp = ".tmp" in script_content

    assert has_rename and has_tmp, "The script does not appear to use an atomic write approach (writing to a .tmp file and renaming)."