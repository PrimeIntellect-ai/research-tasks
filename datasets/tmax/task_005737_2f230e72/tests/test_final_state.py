# test_final_state.py
import os
import pytest

def test_patch_applied():
    """Test that the patch was applied to main.c."""
    main_c_path = "/home/user/release/main.c"
    assert os.path.isfile(main_c_path), f"{main_c_path} does not exist."
    with open(main_c_path, "r") as f:
        content = f.read()
    assert "getline" in content, "The patch does not appear to be applied (missing 'getline')."
    assert "char* line = NULL;" in content, "The patch does not appear to be applied (missing 'char* line = NULL;')."

def test_memory_leak_fixed_in_code():
    """Test that the memory leak was fixed in main.c by freeing the line buffer."""
    main_c_path = "/home/user/release/main.c"
    assert os.path.isfile(main_c_path), f"{main_c_path} does not exist."
    with open(main_c_path, "r") as f:
        content = f.read()
    assert "free(line);" in content, "The memory leak fix 'free(line);' was not found in main.c."

def test_compilation_successful():
    """Test that the project was compiled successfully."""
    executable_path = "/home/user/release/data_processor"
    assert os.path.isfile(executable_path), f"Compiled executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."

def test_processed_output():
    """Test that the processed output contains the correct sum."""
    output_path = "/home/user/release/processed_output.txt"
    assert os.path.isfile(output_path), f"{output_path} does not exist."
    with open(output_path, "r") as f:
        content = f.read().strip()
    assert "Sum: 66" in content, f"Expected 'Sum: 66' in {output_path}, but got: {content}"

def test_valgrind_report():
    """Test that the valgrind report indicates no memory leaks."""
    report_path = "/home/user/release/valgrind_report.txt"
    assert os.path.isfile(report_path), f"{report_path} does not exist."
    with open(report_path, "r") as f:
        content = f.read()

    success_indicators = [
        "All heap blocks were freed",
        "0 bytes in 0 blocks"
    ]

    assert any(indicator in content for indicator in success_indicators), \
        "valgrind_report.txt does not indicate that all heap blocks were freed."