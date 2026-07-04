# test_final_state.py
import os
import pytest

def test_output_file_exists():
    assert os.path.isfile("/home/user/data/output.csv"), "/home/user/data/output.csv does not exist"

def test_output_file_content():
    output_path = "/home/user/data/output.csv"

    # Check that it is valid UTF-8
    try:
        with open(output_path, "rb") as f:
            content = f.read()
            text = content.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail("output.csv is not valid UTF-8")

    expected_lines = [
        "1,René,Boss",
        "3,Françoise,Dev",
        "5,Günter,Admin",
        "8,Gunterxy,AdminDup3",
        "9,João,User"
    ]

    actual_lines = [line.strip() for line in text.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Output file content does not match expected. Got: {actual_lines}"

def test_c_source_and_executable_exist():
    assert os.path.isfile("/home/user/dedup.c"), "C source code /home/user/dedup.c does not exist"
    assert os.path.isfile("/home/user/dedup"), "Executable /home/user/dedup does not exist"
    assert os.access("/home/user/dedup", os.X_OK), "/home/user/dedup is not executable"