# test_final_state.py
import os
import pytest

def test_merged_output_exists():
    assert os.path.isfile("/home/user/merged_output.txt"), "The output file /home/user/merged_output.txt does not exist."

def test_merged_output_content():
    expected_content = "Record 1: Alpha\nRecord 2: Beta\nRecord 3: Gamma\n"

    try:
        with open("/home/user/merged_output.txt", "r", encoding="utf-8") as f:
            actual_content = f.read()
    except UnicodeDecodeError:
        pytest.fail("The output file /home/user/merged_output.txt is not properly UTF-8 encoded.")

    assert actual_content.strip() == expected_content.strip(), "The content of /home/user/merged_output.txt does not match the expected output."

def test_c_source_code_exists_and_uses_flock():
    source_path = "/home/user/merge_dataset.c"
    assert os.path.isfile(source_path), f"The C source file {source_path} does not exist."

    with open(source_path, "r", encoding="utf-8", errors="ignore") as f:
        source_code = f.read()

    assert "flock" in source_code, "The C source code does not use 'flock' as required for concurrency safety."

def test_executable_exists():
    exec_path = "/home/user/merge_dataset"
    assert os.path.isfile(exec_path), f"The executable file {exec_path} does not exist."
    assert os.access(exec_path, os.X_OK), f"The file {exec_path} is not executable."